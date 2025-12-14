"""
Dashboard Component Prompts
Instructions for creating interactive Dashboard elements (Controls, Text).
"""

MARKDOWN_PROMPT = """
To create a Static Markdown Panel:

TYPE: "visualization" with visState.type: "markdown"

CRITICAL STRUCTURE:
{
  "attributes": {
    "title": "Panel Title",
    "visState": "{\"title\":\"Panel Title\",\"type\":\"markdown\",\"params\":{\"fontSize\":12,\"openLinksInNewTab\":false,\"markdown\":\"## Sample Data\\nThis dashboard contains sample data.\"},\"aggs\":[]}",
    "uiStateJSON": "{}",
    "description": "",
    "version": 1,
    "kibanaSavedObjectMeta": {
      "searchSourceJSON": "{\"query\":{\"query\":\"\",\"language\":\"kuery\"},\"filter\":[]}"
    }
  },
  "references": []
}

PARAMS:
- markdown: String with GitHub Flavored Markdown
  - Supports: Headers (##), Lists, Links, Bold, Italic, Code blocks
  - Example: "## Title\\n\\nSome **bold** text and [link](https://example.com)"
- fontSize: Number (default: 12)
- openLinksInNewTab: Boolean (default: false)

NOTE: visState must be stringified JSON, not a JSON object
"""

INPUT_CONTROL_PROMPT = """
To create Dashboard Input Controls (Filter Dropdowns/Sliders):

TYPE: "visualization" with visState.type: "input_control_vis"

CRITICAL STRUCTURE:
{
  "attributes": {
    "title": "Controls",
    "visState": "{\"title\":\"Controls\",\"type\":\"input_control_vis\",\"params\":{\"controls\":[{\"id\":\"1\",\"type\":\"list\",\"fieldName\":\"category.keyword\",\"label\":\"Category\",\"options\":{\"multiselect\":true,\"dynamicOptions\":true,\"type\":\"terms\",\"size\":5},\"indexPatternRefName\":\"control_0_index_pattern\"}],\"updateFiltersOnChange\":true,\"useTimeFilter\":true,\"pinFilters\":false},\"aggs\":[]}",
    "uiStateJSON": "{}",
    "description": "",
    "version": 1,
    "kibanaSavedObjectMeta": {
      "searchSourceJSON": "{\"query\":{\"query\":\"\",\"language\":\"kuery\"},\"filter\":[]}"
    }
  },
  "references": [{
    "name": "control_0_index_pattern",
    "type": "index-pattern",
    "id": "<index-pattern-id>"
  }]
}

CONTROL TYPES:

1. LIST CONTROL (Dropdown):
{
  "id": "1",
  "type": "list",
  "fieldName": "category.keyword",  // Must be keyword field
  "label": "Filter by Category",
  "options": {
    "multiselect": true,
    "dynamicOptions": true,
    "type": "terms",
    "size": 5
  },
  "indexPatternRefName": "control_0_index_pattern"
}

2. RANGE CONTROL (Slider):
{
  "id": "2",
  "type": "range",
  "fieldName": "price",  // Must be numeric field
  "label": "Price Range",
  "options": {
    "decimalPlaces": 0,
    "step": 1
  },
  "indexPatternRefName": "control_1_index_pattern"
}

CRITICAL:
- Each control needs indexPatternRefName matching a reference
- fieldName must match field type (keyword for list, number for range)
- updateFiltersOnChange: true applies filters immediately
- useTimeFilter: true respects time picker
"""

TSVB_MARKDOWN_PROMPT = """
To create Dynamic Markdown (TSVB) with Data Injection:

TYPE: "visualization" with visState.type: "metrics"

CRITICAL STRUCTURE:
{
  "attributes": {
    "title": "Dynamic Markdown",
    "visState": "{\"title\":\"Dynamic Markdown\",\"type\":\"metrics\",\"params\":{\"type\":\"markdown\",\"markdown\":\"Total: {{ count.last.value }}\",\"series\":[{\"id\":\"count\",\"metrics\":[{\"id\":\"count-metric\",\"type\":\"count\"}],\"split_mode\":\"everything\"}],\"time_field\":\"@timestamp\",\"index_pattern\":\"*\"},\"aggs\":[]}",
    "uiStateJSON": "{}",
    "description": "",
    "version": 1,
    "kibanaSavedObjectMeta": {
      "searchSourceJSON": "{\"query\":{\"query\":\"\",\"language\":\"kuery\"},\"filter\":[]}"
    }
  },
  "references": []
}

HANDLEBARS SYNTAX:
- {{ seriesId.last.value }}: Last value
- {{ seriesId.last.formatted }}: Formatted last value
- {{ seriesId.min }}: Minimum value
- {{ seriesId.max }}: Maximum value
- {{ seriesId.avg }}: Average value

SERIES CONFIGURATION:
{
  "id": "count",
  "metrics": [{
    "id": "count-metric",
    "type": "count" | "sum" | "avg" | "max" | "min"
  }],
  "split_mode": "everything" | "terms" | "filters",
  "terms_field": "category.keyword",  // if split_mode: terms
  "terms_size": 10
}

EXAMPLE MARKDOWN:
"## Sales Dashboard\\n\\nTotal Orders: **{{ orders.last.value }}**\\nRevenue: **{{ revenue.last.formatted }}**\\nAverage: {{ revenue.avg }}"
"""

DASHBOARD_PROMPTS = {
    "dashboard_markdown": MARKDOWN_PROMPT,
    "dashboard_input_control": INPUT_CONTROL_PROMPT,
    "dashboard_tsvb_markdown": TSVB_MARKDOWN_PROMPT
}
