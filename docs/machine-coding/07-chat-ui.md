# Chat UI

Messaging thread: message list, composer, optimistic send, stick-to-bottom scroll, and failure/retry. Pairs with [FE Chat design](/frontend-system-design/03-chat).

## Requirements

### Functional

- Render messages in chronological order
- Composer: text + Send (Enter to send, Shift+Enter newline)
- Optimistic append with `clientId`; reconcile on ack
- Failed sends show retry
- Auto-scroll to bottom when pinned; “New messages” when scrolled up
- Optional: load older messages when scrolling to top

### Non-functional

- Don’t jump scroll when prepending history
- Deduplicate realtime + HTTP
- a11y: `role="log"`, labeled composer

### Clarify

- WS vs polling?
- Markdown / reactions / receipts?
- Group vs 1:1?

## Architecture

```mermaid
flowchart TB
  subgraph ui [ChatPanel]
    Header
    MsgList[MessageList]
    Pill[New messages pill]
    Composer
  end
  MsgList --> State[messages by id]
  Composer -->|optimistic| State
  WS[Realtime] -->|upsert| State
  API[sendMessage] -->|ack / fail| State
```

```mermaid
sequenceDiagram
  participant U as User
  participant UI as UI state
  participant API as API
  U->>UI: send text
  UI->>UI: append pending clientId
  UI->>API: POST /messages
  alt ok
    API-->>UI: server message
    UI->>UI: replace pending → confirmed
  else error
    API-->>UI: fail
    UI->>UI: mark failed
  end
```

## Complete implementation

```tsx
// chat-ui.tsx
import {
  useCallback,
  useEffect,
  useLayoutEffect,
  useRef,
  useState,
  type FormEvent,
  type KeyboardEvent,
  type UIEvent,
} from 'react'

export type MsgStatus = 'pending' | 'sent' | 'failed'

export type ChatMessage = {
  id: string // clientId until ack; then server id
  clientId: string
  text: string
  author: 'me' | 'them'
  createdAt: number
  status: MsgStatus
}

function cid() {
  return `c_${Date.now()}_${Math.random().toString(36).slice(2, 8)}`
}

async function apiSend(
  text: string,
  clientId: string,
): Promise<{ id: string; createdAt: number }> {
  const res = await fetch('/api/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text, clientId }),
  })
  if (!res.ok) throw new Error('Send failed')
  return res.json()
}

const NEAR_BOTTOM_PX = 80

export function ChatUI({
  initial = [],
  meLabel = 'You',
}: {
  initial?: ChatMessage[]
  meLabel?: string
}) {
  const [messages, setMessages] = useState<ChatMessage[]>(initial)
  const [draft, setDraft] = useState('')
  const [pinned, setPinned] = useState(true)
  const [unseen, setUnseen] = useState(0)

  const scrollerRef = useRef<HTMLDivElement>(null)
  const bottomRef = useRef<HTMLDivElement>(null)
  const prevHeight = useRef(0)

  const scrollToBottom = useCallback((behavior: ScrollBehavior = 'smooth') => {
    bottomRef.current?.scrollIntoView({ behavior })
  }, [])

  const onScroll = (e: UIEvent<HTMLDivElement>) => {
    const el = e.currentTarget
    const distance = el.scrollHeight - el.scrollTop - el.clientHeight
    const near = distance < NEAR_BOTTOM_PX
    setPinned(near)
    if (near) setUnseen(0)
  }

  // Stick to bottom on new messages when pinned
  useLayoutEffect(() => {
    if (pinned) {
      scrollToBottom(messages.length <= 1 ? 'auto' : 'smooth')
    }
  }, [messages, pinned, scrollToBottom])

  const upsertIncoming = useCallback(
    (msg: ChatMessage) => {
      setMessages((prev) => {
        if (prev.some((m) => m.id === msg.id || m.clientId === msg.clientId)) {
          return prev.map((m) =>
            m.clientId === msg.clientId || m.id === msg.id ? { ...m, ...msg } : m,
          )
        }
        return [...prev, msg]
      })
      if (!pinned && msg.author === 'them') {
        setUnseen((n) => n + 1)
      }
    },
    [pinned],
  )

  // Fake peer / WS hook point
  useEffect(() => {
    const t = setInterval(() => {
      // demo only — replace with WebSocket onmessage
    }, 60_000)
    return () => clearInterval(t)
  }, [])

  const send = async (text: string) => {
    const trimmed = text.trim()
    if (!trimmed) return
    const clientId = cid()
    const optimistic: ChatMessage = {
      id: clientId,
      clientId,
      text: trimmed,
      author: 'me',
      createdAt: Date.now(),
      status: 'pending',
    }
    setMessages((prev) => [...prev, optimistic])
    setDraft('')
    setPinned(true)
    setUnseen(0)

    try {
      const ack = await apiSend(trimmed, clientId)
      setMessages((prev) =>
        prev.map((m) =>
          m.clientId === clientId
            ? { ...m, id: ack.id, createdAt: ack.createdAt, status: 'sent' }
            : m,
        ),
      )
    } catch {
      setMessages((prev) =>
        prev.map((m) => (m.clientId === clientId ? { ...m, status: 'failed' } : m)),
      )
    }
  }

  const retry = async (clientId: string) => {
    const msg = messages.find((m) => m.clientId === clientId)
    if (!msg) return
    setMessages((prev) =>
      prev.map((m) => (m.clientId === clientId ? { ...m, status: 'pending' } : m)),
    )
    try {
      const ack = await apiSend(msg.text, clientId)
      setMessages((prev) =>
        prev.map((m) =>
          m.clientId === clientId
            ? { ...m, id: ack.id, createdAt: ack.createdAt, status: 'sent' }
            : m,
        ),
      )
    } catch {
      setMessages((prev) =>
        prev.map((m) => (m.clientId === clientId ? { ...m, status: 'failed' } : m)),
      )
    }
  }

  /** Call before prepending history; restores visual position */
  const prependHistory = (older: ChatMessage[]) => {
    const el = scrollerRef.current
    if (el) prevHeight.current = el.scrollHeight
    setMessages((prev) => {
      const seen = new Set(prev.map((m) => m.id))
      const merged = [...older.filter((m) => !seen.has(m.id)), ...prev]
      return merged
    })
  }

  useLayoutEffect(() => {
    const el = scrollerRef.current
    if (!el || prevHeight.current === 0) return
    const delta = el.scrollHeight - prevHeight.current
    el.scrollTop += delta
    prevHeight.current = 0
  }, [messages])

  const onSubmit = (e: FormEvent) => {
    e.preventDefault()
    void send(draft)
  }

  const onKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      void send(draft)
    }
  }

  return (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        height: 480,
        border: '1px solid #ccc',
        maxWidth: 420,
      }}
    >
      <header style={{ padding: 8, borderBottom: '1px solid #eee' }}>Chat</header>

      <div style={{ position: 'relative', flex: 1, minHeight: 0 }}>
        <div
          ref={scrollerRef}
          role="log"
          aria-live="polite"
          aria-relevant="additions"
          onScroll={onScroll}
          style={{ height: '100%', overflow: 'auto', padding: 8 }}
        >
          <button type="button" onClick={() => prependHistory([])}>
            {/* wire to fetch older */}
            Load older
          </button>
          {messages.map((m) => (
            <div
              key={m.clientId}
              style={{
                display: 'flex',
                justifyContent: m.author === 'me' ? 'flex-end' : 'flex-start',
                marginBottom: 8,
              }}
            >
              <div
                style={{
                  maxWidth: '75%',
                  padding: '8px 10px',
                  borderRadius: 12,
                  background: m.author === 'me' ? '#dcf8c6' : '#f1f0f0',
                  opacity: m.status === 'pending' ? 0.7 : 1,
                }}
              >
                <div>{m.text}</div>
                <div style={{ fontSize: 11, opacity: 0.7 }}>
                  {m.author === 'me' ? meLabel : 'Them'} ·{' '}
                  {m.status === 'pending' && 'Sending…'}
                  {m.status === 'sent' && 'Sent'}
                  {m.status === 'failed' && (
                    <>
                      Failed{' '}
                      <button type="button" onClick={() => void retry(m.clientId)}>
                        Retry
                      </button>
                    </>
                  )}
                </div>
              </div>
            </div>
          ))}
          <div ref={bottomRef} />
        </div>

        {unseen > 0 && (
          <button
            type="button"
            onClick={() => {
              setPinned(true)
              setUnseen(0)
              scrollToBottom()
            }}
            style={{
              position: 'absolute',
              bottom: 8,
              left: '50%',
              transform: 'translateX(-50%)',
            }}
          >
            {unseen} new message{unseen > 1 ? 's' : ''}
          </button>
        )}
      </div>

      <form onSubmit={onSubmit} style={{ display: 'flex', gap: 8, padding: 8 }}>
        <label className="sr-only" htmlFor="chat-draft">
          Message
        </label>
        <textarea
          id="chat-draft"
          rows={2}
          value={draft}
          onChange={(e) => setDraft(e.target.value)}
          onKeyDown={onKeyDown}
          placeholder="Message"
          style={{ flex: 1, resize: 'none' }}
        />
        <button type="submit" disabled={!draft.trim()}>
          Send
        </button>
      </form>
    </div>
  )
}

// Expose for WS integration demos
export type { ChatMessage as Message }
```

### Realtime merge sketch

```ts
socket.onmessage = (ev) => {
  const msg = JSON.parse(ev.data) as ChatMessage
  upsertIncoming({ ...msg, status: 'sent' })
}
```

## Edge cases

| Case | Handling |
| --- | --- |
| Double ack (HTTP + WS) | Dedupe by `clientId` / server `id` |
| User scrolled up + own send | Usually force pin on send |
| Prepend history | Adjust `scrollTop` by height delta |
| Empty send / whitespace | Ignore |
| Very long message | CSS wrap; server max length |
| Reconnect backlog | Resume cursor; merge sorted |
| `aria-live` spam | polite + don’t announce every keystroke |

## Follow-up interview questions

1. How do you preserve scroll when loading older messages?
2. Optimistic UI rollback patterns?
3. Virtualize a chat list — what’s hard about stick-to-bottom?
4. Exactly-once delivery vs at-least-once on WS?
5. Where does typing indicator live (ephemeral)?
6. How to order messages with clock skew?
7. Offline queue design?
8. E2E encryption impact on search/preview?

## Common mistakes

| Mistake | Fix |
| --- | --- |
| Key = array index | Use `clientId` |
| Auto-scroll always | Respect `pinned` |
| Replace entire list on WS event | Upsert |
| Blocking send button until ack only | Allow queue; show pending |
| Prepend without scroll adjust | Jump |
| Putting draft in global store | Local state |

## Trade-offs

| Choice | Pros | Cons |
| --- | --- | --- |
| Optimistic send | Feels instant | Reconcile complexity |
| Virtualize | Long history OK | Sticky bottom harder |
| WS + HTTP send | Reliable ack | Dedupe required |
| Polling | Simple | Latency / cost |

**Interview close:** “Optimistic pending row keyed by `clientId`, reconcile on ack, stick-to-bottom when pinned, height-delta when prepending history.”

## Related

- [FE Chat](/frontend-system-design/03-chat) · [BE Chat](/backend-system-design/03-chat)
- [Infinite scroll](/machine-coding/03-infinite-scroll) · [Virtual list](/machine-coding/04-virtual-list)
