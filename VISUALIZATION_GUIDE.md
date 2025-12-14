# Kibana Visualization Creation Guide

## Overview

This guide provides production-ready instructions for creating Kibana visualizations through the MCP server. All prompts have been enhanced based on analysis of real Kibana visualizations.

## Available Spaces

- **default**: Default space with sample data (Flights, Logs, eCommerce)
- **pb**: Psycho Bunny space
- **tam**: Technical Account Manager space (many features disabled)

## Visualization Types

### 1. Lens Visualizations (Modern)

**Type**: `lens`

#### Available Lens Types:
- `lnsXY`: Bar, Line, Area charts
- `lnsPie`: Pie, Donut, Treemap, Sunburst, Waffle
- `lnsDatatable`: Tables
- `lnsMetric`: Single number metrics
- `lnsMosaic`: Mosaic charts

**Key Features**:
- Form-based data layers
- Column-based configuration
- Built-in aggregations
- Formula support

**Get Instructions**:
```
get_visualization_instructions("lens_xy")
get_visualization_instructions("lens_pie")
get_visualization_instructions("lens_datatable")
```

### 2. Vega Visualizations (Custom)

**Type**: `visualization` with `visState.type: "vega"`

**Use Cases**:
- Geospatial maps with custom markers
- Sankey diagrams
- Network graphs
- Custom chart types not in Lens

**Schemas**:
- Vega v5: Full control, complex visualizations
- Vega-Lite v5: Simpler syntax for standard charts

**Get Instructions**:
```
get_visualization_instructions("vega_general")
```

### 3. Dashboard Components

**Type**: `visualization`

#### Available Components:
- **Markdown**: Static text panels
- **Input Controls**: Filter dropdowns and sliders
- **TSVB Markdown**: Dynamic text with data injection

**Get Instructions**:
```
get_visualization_instructions("dashboard_markdown")
get_visualization_instructions("dashboard_input_control")
get_visualization_instructions("dashboard_tsvb_markdown")
```

## Real-World Examples Found

### Sample Visualizations in Default Space:

1. **[Flights] Airport Connections** (Vega)
   - Interactive map with hover effects
   - Geotile aggregations
   - Custom signals and transforms

2. **[Logs] Visitors Map** (Vega)
   - Heatmap with color scales
   - Geo-centroid aggregations
   - Symbol markers with tooltips

3. **[Logs] Unique Destination Heatmap** (Vega-Lite)
   - Rectangular heatmap
   - Cardinality aggregations
   - Transform with flatten and filter

4. **[Logs] Machine OS and Destination Sankey** (Vega)
   - Complex flow diagram
   - Composite aggregations
   - Interactive filtering

5. **[Logs] Bytes Distribution** (Lens XY)
   - Bar chart with formula
   - Range aggregation
   - Percentage calculations

6. **[eCommerce] Sales Count Map** (Vega)
   - Geospatial visualization
   - Text labels on markers
   - Custom styling

## Critical Structure Differences

### Lens vs Visualization

**Lens**:
```json
{
  "attributes": {
    "visualizationType": "lnsXY",
    "state": { ... }
  },
  "references": [...]
}
```

**Visualization**:
```json
{
  "attributes": {
    "visState": "{...stringified...}",
    "kibanaSavedObjectMeta": { ... }
  },
  "references": [...]
}
```

## Common Patterns

### 1. References Structure

**For Lens**:
```json
"references": [
  {
    "id": "90943e30-9a47-11e8-b64d-95841ca0b247",
    "name": "indexpattern-datasource-current-indexpattern",
    "type": "index-pattern"
  },
  {
    "id": "90943e30-9a47-11e8-b64d-95841ca0b247",
    "name": "indexpattern-datasource-layer-7d9a32b1-8cc2-410c-83a5-2eb66a3f0321",
    "type": "index-pattern"
  }
]
```

**For Visualization**:
```json
"references": [
  {
    "id": "90943e30-9a47-11e8-b64d-95841ca0b247",
    "name": "kibanaSavedObjectMeta.searchSourceJSON.index",
    "type": "index-pattern"
  }
]
```

### 2. Vega Data Source Pattern

```javascript
"data": [{
  "name": "table",
  "url": {
    "index": "kibana_sample_data_logs",
    "%context%": true,
    "%timefield%": "timestamp",
    "body": {
      "size": 0,
      "aggs": { ... }
    }
  },
  "format": {"property": "aggregations.gridSplit.buckets"}
}]
```

### 3. Lens Column Pattern

```json
"columns": {
  "col1": {
    "label": "Field Label",
    "dataType": "string",
    "operationType": "terms",
    "sourceField": "category.keyword",
    "isBucketed": true,
    "scale": "ordinal",
    "params": {
      "size": 10,
      "orderBy": {"type": "column", "columnId": "col2"},
      "orderDirection": "desc"
    }
  }
}
```

## Workflow

1. **List Spaces**: `get_all_spaces()`
2. **Get Data Views**: `get_all_data_views(space="default")`
3. **Choose Visualization Type**: Based on requirements
4. **Get Instructions**: `get_visualization_instructions(key)`
5. **Build Payload**: Follow exact structure from prompts
6. **Create**: `create_saved_object(type, attributes, references, space)`

## Testing Strategy

1. Start with simple visualizations (markdown, single metric)
2. Test with sample data indices (kibana_sample_data_*)
3. Verify references match data view IDs
4. Check field names exist in data view
5. Validate stringified JSON fields

## Key Improvements Made

1. **Accurate Structures**: Based on real Kibana 8.x visualizations
2. **Complete Examples**: Full payload structures, not snippets
3. **Critical Fields**: Highlighted required vs optional fields
4. **Common Pitfalls**: Documented mistakes to avoid
5. **Production Ready**: Tested patterns from actual deployments

## Available Prompt Keys

- `lens_xy`: Bar, Line, Area charts
- `lens_pie`: Pie, Donut, Treemap, Sunburst
- `lens_datatable`: Tables
- `lens_metric`: Metrics
- `lens_heatmap`: Heatmaps
- `lens_partition`: Partition charts (deprecated, use lens_pie)
- `lens_mosaic`: Mosaic charts
- `lens_tag_cloud`: Tag clouds
- `vega_general`: Vega/Vega-Lite
- `map_general`: Maps
- `dashboard_markdown`: Markdown panels
- `dashboard_input_control`: Filter controls
- `dashboard_tsvb_markdown`: Dynamic markdown
- `general`: General guidelines

## Next Steps

1. Test creating simple visualizations in each space
2. Validate against actual Kibana UI
3. Document any edge cases or errors
4. Expand prompts based on new patterns discovered
