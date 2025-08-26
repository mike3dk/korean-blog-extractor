# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

- **Install dependencies**: `poetry install`
- **Run tests**: `pytest` or `pytest tests/`
- **Run specific test**: `pytest tests/test_post_handler.py::test_post_handler`
- **Format code**: `black korean_blog_extractor/`
- **Manual testing script**: `python scripts/test/run_posts.py` (tests against real URLs)
- **BlogChart testing script**: `python scripts/test/run_blogchart.py`

## Architecture Overview

This is a Python package for extracting blog information from Korean blog platforms (Naver, Tistory, WordPress). The codebase follows a plugin-based architecture:

### Core Components

- **PostHandler** (`korean_blog_extractor/post_handler.py`): Main entry point that analyzes URLs, determines platform, and coordinates extraction
- **BlogChartHandler** (`korean_blog_extractor/blog_chart_handler.py`): Extracts blogger rankings from blogchart.co.kr
- **Platform modules** (`korean_blog_extractor/platforms/`): Individual extractors for each blog platform
  - `naver.py`: Handles Naver blog extraction
  - `tistory.py`: Handles Tistory blog extraction  
  - `wordpress.py`: Handles WordPress blog extraction
  - `common.py`: Shared utilities (BeautifulSoup fetching)

### Key Design Patterns

- **Strategy pattern**: Platform-specific extraction functions are mapped in `func_dict_blog_info` and `func_dict_tags_images` dictionaries
- **RSS-based detection**: Platforms are identified by RSS URL patterns and feed metadata
- **Two-phase extraction**: 
  1. URL analysis and RSS discovery in `__guess_rss_url()`
  2. Content extraction via `extract()` method using platform-specific functions

### Data Flow

1. `PostHandler.__init__()` → URL validation and platform detection
2. `PostHandler.extract()` → RSS parsing and platform-specific extraction
3. Platform functions return blog info and extract tags/images from post content
4. Results accessible via properties: `blog_info`, `post_tags_images`

## Testing Strategy

- Unit tests use mocked RSS feeds and HTML content from `tests/data/`
- Integration tests via `scripts/test/run_posts.py` hit real URLs
- Expected outputs stored in `scripts/test/expected_posts.yaml`
- All tests parameterized across supported platforms (Naver, Tistory, WordPress)