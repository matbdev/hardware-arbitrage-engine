# OLX Data Extraction Guide

Based on the analysis of `index.html`, here is a guide on how to extract the key information you need. The page uses many dynamic and generated CSS classes (like `ad__sc-1l883pa-0`), so it's safer to rely on `id` attributes or specific `data-*` attributes where possible.

## Selectors & Extraction Logic

### 1. First Picture
- **Selector**: `button#item-gallery-image picture img` or `img[data-display="multi"]`
- **Action**: Extract the `src` attribute of the first matched element.
- **Example**: `document.querySelector('button#item-gallery-image picture img').src`

### 2. Title
- **Selector**: `#description-title span.typo-title-medium`
- **Action**: Extract the `innerText` or `textContent`.
- **Note**: The title is located inside the `#description-title` container.

### 3. Description
- **Selector**: `[data-section="description"]` or `#description-title [data-section="description"] span`
- **Action**: Extract the `innerText` or `textContent`.
- **Note**: This will give you the full multiline text of the ad description.

### 4. Price
- **Selector**: `#price-box-container .typo-title-large`
- **Action**: Extract the `innerText` (e.g., "R$ 388").
- **Note**: The `#price-box-container` also contains the original price (if discounted) and installment info if you need it in the future.

### 5. Seller Information (Name, Stars)
- **Observation**: In the provided static HTML, the seller profile box contains skeleton loaders (e.g., `<div aria-busy="true" class="olx-skeleton">`). This indicates that **the seller name and information are loaded dynamically via Javascript/API** after the initial HTML load.
- **Recommendation**: Since the seller data isn't in the static HTML source, you will need to either:
  1. Use a headless browser (like Puppeteer, Playwright, or Selenium) to wait for the seller information to render.
  2. Intercept the background API requests (XHR/Fetch) that OLX makes to fetch the ad details.

### 6. Location (Useful for the future)
- **Selector**: `#location div.flex.flex-col span`
- **Action**: Extract the text of these spans.
- **Note**: There are usually two spans here. The first contains the neighborhood/area (e.g., "Vila Nova"), and the second contains the City, State, and ZIP Code (e.g., "Rancharia, SP, 19600426").

### 7. Extra Details (Category, Condition, Type, etc.)
- **Selector**: `#details div[data-ds-component="DS-Container"]`
- **Action**: Loop through each container. Inside, you can find the label (`span.typo-overline`) and the value (`a.olx-link` or `span`).
- **Example Use**: You can extract that the "Condição" (Condition) is "Novo" (New).
