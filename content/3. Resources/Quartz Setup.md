---
title: Quartz Setup
tags:
  - quartz
---
# 작업 순서

1. Download node js 
	1. **at least [Node](https://nodejs.org/) v18.14** and `npm` v9.3.1 to function correctly. Ensure you have this installed on your machine before continuing.
2. git clone repo
	1. Choose how to initialize the content in `/Users/yoonjungrho/rho_work/quartz/content` 
		1. Empty Quartz
	2. Choose how Quartz should resolve links in your content. You can change this later in `quartz.config.ts`. 
		1. Treat links as shortest path
	3. You're all set! Not sure what to do next? Try:
		1. Customizing Quartz a bit more by editing `quartz.config.ts`
		2. Running `npx quartz build --serve` to preview your Quartz locally
		3. Hosting your Quartz online (see: https://quartz.jzhao.xyz/hosting)
3. Write or make changes in content folder 
4. In your local Quartz, create a new file `quartz/.github/workflows/deploy.yml`.
5. Using github desktop add repository
6. Change settings > pages > git hub actions
7. Rerun if failed

❯ npx quartz build --serve
```
git clone https://github.com/jackyzha0/quartz.git
cd quartz
npm i
npx quartz create
```