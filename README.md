# Senior Full-Stack Interview Handbook

VitePress handbook for mid → senior full-stack interviews.

## Local

```bash
npm install
npm run dev      # http://localhost:5173/FullstackPreparation/
npm run build
npm run preview
```

Content lives under `docs/`.

## Deploy (GitHub Pages)

Site URL after deploy:

**https://prajjwaljogdand.github.io/FullstackPreparation/**

### One-time setup in GitHub

1. Open the repo → **Settings** → **Pages**
2. Under **Build and deployment** → **Source**, choose **GitHub Actions**
3. Push to `main` (or run the **Deploy VitePress to GitHub Pages** workflow manually under **Actions**)

The workflow [`.github/workflows/deploy-docs.yml`](.github/workflows/deploy-docs.yml) builds VitePress and publishes `docs/.vitepress/dist`.

`base` in [`docs/.vitepress/config.ts`](docs/.vitepress/config.ts) is set to `/FullstackPreparation/` so assets work on project Pages (not a custom root domain).

### If you rename the repo

Update `base` in `docs/.vitepress/config.ts` to match:

```ts
base: '/YourRepoName/',
```
