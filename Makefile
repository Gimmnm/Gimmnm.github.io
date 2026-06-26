.PHONY: serve build clean deploy-check

serve:
	hugo server -D --disableFastRender

build:
	hugo --minify

clean:
	hugo -D --minify 2>&1 | tail -5
	rm -rf public/

deploy-check: build
	@grep -rl 'katex.min.css' public/ | head -1 | xargs test -f && echo "OK: KaTeX CSS found"
	@grep -rl 'renderMathInElement' public/ | head -1 | xargs test -f && echo "OK: KaTeX auto-render found"
	@grep -c 'katex-display' public/posts/basic-diffusion-model/index.html 2>/dev/null || true
