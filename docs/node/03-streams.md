# Streams

Streams process data **incrementally** — bounded memory, backpressure, composable pipelines. Interview signal: you understand **Readable/Writable modes**, `pipe` vs `pipeline`, and why ignoring backpressure OOMs production boxes.

Related: [Buffers](/node/04-buffers) · [Performance](/node/11-performance) · [File/CDN design](/backend-system-design/06-file-cdn)

## Stream types

| Type | Direction | Examples |
| --- | --- | --- |
| Readable | produce | `fs.createReadStream`, HTTP req |
| Writable | consume | `fs.createWriteStream`, HTTP res |
| Duplex | both | TCP socket, `zlib` sometimes framed |
| Transform | Duplex + mutate | `zlib.createGzip`, crypto cipher |

```mermaid
flowchart LR
  R[Readable] -->|chunks| T[Transform]
  T --> W[Writable]
  W -.->|backpressure| T
  T -.->|backpressure| R
```

## Object mode vs binary

Default: `Buffer` / `Uint8Array` chunks (or strings if decoded). `objectMode: true` allows arbitrary JS values — useful for NDJSON parsers; don’t mix carelessly with binary sinks.

```ts
import { Transform } from 'node:stream'

const toLines = new Transform({
  readableObjectMode: true,
  transform(chunk, _enc, cb) {
    const text = chunk.toString('utf8')
    for (const line of text.split('
')) {
      if (line) this.push({ line })
    }
    cb()
  },
})
```

## Flowing vs paused (Readable)

- **Paused (default historically):** you call `read()`, or attach `'data'` which switches to flowing.
- **Flowing:** emits `'data'` as fast as possible — **must** handle or pause, or buffer grows.
- Prefer **async iteration** / `pipeline` over raw `'data'` handlers.

```ts
import fs from 'node:fs'
import { createInterface } from 'node:readline'

// Async iteration — respects backpressure with modern streams
async function countLines(path: string) {
  let n = 0
  const rl = createInterface({ input: fs.createReadStream(path), crlfDelay: Infinity })
  for await (const _line of rl) n++
  return n
}
```

## Backpressure

When writable buffer exceeds `highWaterMark`, `write()` returns `false`. You must wait for `'drain'`.

```ts
import type { Writable } from 'node:stream'

async function writeAll(writable: Writable, chunks: Buffer[]) {
  for (const chunk of chunks) {
    if (!writable.write(chunk)) {
      await new Promise<void>((resolve) => writable.once('drain', resolve))
    }
  }
  await new Promise<void>((resolve, reject) => {
    writable.end(() => resolve())
    writable.on('error', reject)
  })
}
```

`highWaterMark` defaults: **64 KiB** for byte streams, **16** objects in objectMode — tune carefully.

## `pipe` vs `pipeline`

`readable.pipe(writable)` does not forward errors well and won’t destroy the whole chain on failure. **`stream.pipeline` / `streamPromises.pipeline`** destroys streams on error and invokes a final callback/promise.

```ts
import { createReadStream, createWriteStream } from 'node:fs'
import { createGzip } from 'node:zlib'
import { pipeline } from 'node:stream/promises'

await pipeline(
  createReadStream('in.bin'),
  createGzip(),
  createWriteStream('out.gz'),
)
```

```ts
import http from 'node:http'
import { createReadStream } from 'node:fs'
import { pipeline } from 'node:stream/promises'

http.createServer(async (req, res) => {
  try {
    res.setHeader('Content-Type', 'application/octet-stream')
    await pipeline(createReadStream('/var/data/big.bin'), res)
  } catch {
    if (!res.headersSent) res.writeHead(500)
    res.end()
  }
}).listen(3000)
```

## Implementing a Transform

```ts
import { Transform, type TransformCallback } from 'node:stream'

class UpperCase extends Transform {
  _transform(chunk: Buffer, _enc: BufferEncoding, cb: TransformCallback) {
    try {
      cb(null, Buffer.from(chunk.toString('utf8').toUpperCase()))
    } catch (err) {
      cb(err as Error)
    }
  }
}
```

## Error & destroy semantics

- Always attach `'error'` or use `pipeline`.
- `stream.destroy(err)` aborts; cleanup in `_destroy`.
- HTTP: if client aborts, destroy the readable to stop disk/CPU waste.

```ts
req.on('close', () => {
  if (!req.complete) readable.destroy()
})
```

## Interview Q&A

**Q: Why not `fs.readFile` for multi-GB files?**  
A: Loads entire file into RAM. Streams keep memory ≈ `highWaterMark` × stages.

**Q: What does `write()` returning `false` mean?**  
A: Buffer full — apply backpressure; wait for `'drain'` before writing more.

**Q: `pipe` vs `pipeline`?**  
A: Prefer `pipeline` for error propagation and cleanup. `pipe` is easy to leak / hang.

**Q: Duplex vs Transform?**  
A: Duplex = independent read/write sides (socket). Transform = write input becomes read output (filter).

**Q: How do streams relate to HTTP chunked encoding?**  
A: Response can be streamed; Transfer-Encoding chunked when length unknown. See [API Design](/backend/01-api-design).

## Common Mistakes

- Listening to `'data'` without handling backpressure.
- Using `pipe` and ignoring errors → process crash (`uncaughtException`) or hung sockets.
- Buffering entire stream into an array “just this once” in a hot path.
- Forgetting to `end()` writables → consumers hang.
- Mixing sync CPU in `_transform` without yielding → stalls the loop.

## Trade-offs

| Choice | Benefit | Cost |
| --- | --- | --- |
| Low `highWaterMark` | Less RAM | More syscalls / overhead |
| High `highWaterMark` | Throughput | Latency spikes / RAM |
| Object mode | Ergonomic parsing | Serialization cost; easy to retain large graphs |
| `pipeline` | Safe cleanup | Slightly more verbose than `pipe` |
| Stream to client | TTFB / memory | Harder retries; partial failures |

**Production:** Prefer streams for uploads, downloads, proxies, and log shippers. Cap concurrent stream pipelines. For multipart uploads and CDN edges, see [File Upload / CDN](/backend-system-design/06-file-cdn).


## `readableFlowing` & `pause`/`resume`

```ts
const rs = fs.createReadStream('big.bin')
rs.on('data', (chunk) => {
  if (!processChunk(chunk)) rs.pause()
})
emitter.on('ready', () => rs.resume())
```

Async iteration is usually clearer. For HTTP proxying, `pipeline(req, upstream, res)` wires abort signals in modern Node.

## AbortSignal with streams

```ts
import { pipeline } from 'node:stream/promises'

const ac = new AbortController()
setTimeout(() => ac.abort(), 5_000)
await pipeline(readable, transform, writable, { signal: ac.signal })
```

## Custom Readable

```ts
import { Readable } from 'node:stream'

class Counter extends Readable {
  private i = 0
  constructor(private max: number) { super({ objectMode: true }) }
  _read() {
    if (this.i >= this.max) this.push(null)
    else this.push({ n: this.i++ })
  }
}
```

Pushing faster than consumption without respecting backpressure buffers in memory — `_read` should push on demand.
