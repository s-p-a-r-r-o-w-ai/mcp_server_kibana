"""
Lens Visualization Prompts
Contains generalized instruction sets for creating various Lens visualization types.
"""

LENS_XY_PROMPT = """
To create a Lens XY Chart (Bar, Line, Area), use the following structure:

TYPE: "lens" with visualizationType: "lnsXY"

CRITICAL STRUCTURE:
{
  "attributes": {
    "title": "Chart Title",
    "visualizationType": "lnsXY",
    "state": {
      "datasourceStates": {
        "formBased": {
          "layers": {
            "<layer-id>": {
              "columnOrder": ["col1", "col2", "col3"],
              "columns": {
                "col1": {
                  "label": "X-Axis Label",
                  "dataType": "date" | "string" | "number",
                  "operationType": "date_histogram" | "terms" | "range",
                  "sourceField": "timestamp",
                  "isBucketed": true,
                  "scale": "interval" | "ordinal",
                  "params": {
                    "interval": "auto",  // for date_histogram
                    "size": 10,  // for terms
                    "orderBy": {"type": "column", "columnId": "col2"},
                    "orderDirection": "desc"
                  }
                },
                "col2": {
                  "label": "Y-Axis Label",
                  "dataType": "number",
                  "operationType": "count" | "sum" | "average" | "median" | "formula",
                  "sourceField": "bytes",  // omit for count
                  "isBucketed": false,
                  "scale": "ratio",
                  "params": {
                    "format": {"id": "number", "params": {"decimals": 2}}
                  }
                },
                "col3": {  // Optional breakdown
                  "label": "Breakdown",
                  "dataType": "string",
                  "operationType": "terms",
                  "sourceField": "category.keyword",
                  "isBucketed": true,
                  "scale": "ordinal",
                  "params": {"size": 5}
                }
              },
              "incompleteColumns": {}
            }
          }
        }
      },
      "filters": [],
      "query": {"language": "kuery", "query": ""},
      "visualization": {
        "layers": [{
          "layerId": "<layer-id>",
          "accessors": ["col2"],
          "position": "top",
          "seriesType": "bar_stacked" | "line" | "area" | "bar_horizontal",
          "showGridlines": false,
          "xAccessor": "col1",
          "splitAccessor": "col3",  // Optional
          "layerType": "data"
        }],
        "legend": {"isVisible": true, "position": "right", "legendSize": "auto"},
        "preferredSeriesType": "bar_stacked",
        "valueLabels": "hide",
        "fittingFunction": "None",
        "axisTitlesVisibilitySettings": {"x": true, "yLeft": true, "yRight": true},
        "gridlinesVisibilitySettings": {"x": true, "yLeft": true, "yRight": true},
        "tickLabelsVisibilitySettings": {"x": true, "yLeft": true, "yRight": true},
        "yLeftExtent": {"mode": "full"},
        "yRightExtent": {"mode": "full"}
      }
    }
  },
  "references": [{
    "id": "<index-pattern-id>",
    "name": "indexpattern-datasource-current-indexpattern",
    "type": "index-pattern"
  }, {
    "id": "<index-pattern-id>",
    "name": "indexpattern-datasource-layer-<layer-id>",
    "type": "index-pattern"
  }]
}

FORMULA OPERATIONS:
- For complex calculations, use operationType: "formula"
- params.formula: "count() / overall_sum(count())"
- params.isFormulaBroken: false
- Formula creates hidden helper columns (col2X0, col2X1, etc.)
- Main column references the final helper column
"""

LENS_PIE_PROMPT = """
To create a Lens Pie/Donut/Treemap/Sunburst Chart:

TYPE: "lens" with visualizationType: "lnsPie"

CRITICAL: Use "lnsPie" for ALL partition charts (pie, donut, treemap, sunburst, waffle)

STRUCTURE:
{
  "attributes": {
    "title": "Chart Title",
    "visualizationType": "lnsPie",
    "state": {
      "datasourceStates": {
        "formBased": {
          "layers": {
            "<layer-id>": {
              "columnOrder": ["col1", "col2", "col3"],
              "columns": {
                "col1": {  // Primary grouping
                  "label": "Category",
                  "dataType": "string",
                  "operationType": "terms",
                  "sourceField": "category.keyword",
                  "isBucketed": true,
                  "scale": "ordinal",
                  "params": {
                    "size": 10,
                    "orderBy": {"type": "column", "columnId": "col3"},
                    "orderDirection": "desc",
                    "otherBucket": false,
                    "missingBucket": false
                  }
                },
                "col2": {  // Optional: Secondary grouping for hierarchical charts
                  "label": "Subcategory",
                  "dataType": "string",
                  "operationType": "terms",
                  "sourceField": "manufacturer.keyword",
                  "isBucketed": true,
                  "scale": "ordinal",
                  "params": {"size": 10}
                },
                "col3": {  // Metric
                  "label": "Total Sales",
                  "dataType": "number",
                  "operationType": "sum" | "count" | "average",
                  "sourceField": "taxful_total_price",
                  "isBucketed": false,
                  "scale": "ratio",
                  "params": {
                    "format": {"id": "currency", "params": {"decimals": 2}}
                  }
                }
              },
              "incompleteColumns": {},
              "indexPatternId": "<index-pattern-id>"  // REQUIRED
            }
          }
        }
      },
      "filters": [],
      "query": {"language": "kuery", "query": ""},
      "visualization": {
        "shape": "pie" | "donut" | "treemap" | "sunburst" | "waffle",
        "layers": [{
          "layerId": "<layer-id>",
          "primaryGroups": ["col1"],  // For single level
          "primaryGroups": ["col1", "col2"],  // For hierarchical (treemap/sunburst)
          "metrics": ["col3"],
          "numberDisplay": "percent" | "value",
          "categoryDisplay": "default" | "hide",
          "legendDisplay": "default" | "hide" | "show",
          "nestedLegend": false,
          "layerType": "data"
        }]
      }
    }
  },
  "references": [{
    "type": "index-pattern",
    "id": "<index-pattern-id>",
    "name": "indexpattern-datasource-layer-<layer-id>"
  }]
}

SHAPE OPTIONS:
- "pie": Traditional pie chart
- "donut": Donut chart with center hole
- "treemap": Rectangular hierarchical layout
- "sunburst": Radial hierarchical layout
- "waffle": Grid of squares
"""

LENS_DATATABLE_PROMPT = """
To create a Lens Datatable (Table):

TYPE: "lens" with visualizationType: "lnsDatatable"

STRUCTURE:
{
  "attributes": {
    "title": "Data Table",
    "visualizationType": "lnsDatatable",
    "state": {
      "datasourceStates": {
        "formBased": {
          "layers": {
            "<layer-id>": {
              "columnOrder": ["col1", "col2", "col3"],
              "columns": {
                "col1": {  // Dimension column
                  "label": "Category",
                  "dataType": "string",
                  "operationType": "terms",
                  "sourceField": "category.keyword",
                  "isBucketed": true,
                  "scale": "ordinal",
                  "params": {"size": 10}
                },
                "col2": {  // Metric column
                  "label": "Total Sales",
                  "dataType": "number",
                  "operationType": "sum",
                  "sourceField": "sales",
                  "isBucketed": false,
                  "scale": "ratio"
                },
                "col3": {  // Formula column
                  "label": "Conversion %",
                  "dataType": "number",
                  "operationType": "formula",
                  "isBucketed": false,
                  "scale": "ratio",
                  "params": {
                    "formula": "sum(conversions) / sum(visits) * 100",
                    "isFormulaBroken": false,
                    "format": {"id": "percent", "params": {"decimals": 1}}
                  },
                  "references": ["col3X0"]
                }
              },
              "incompleteColumns": {}
            }
          }
        }
      },
      "filters": [],
      "query": {"language": "kuery", "query": ""},
      "visualization": {
        "layerId": "<layer-id>",
        "layerType": "data",
        "columns": [
          {
            "columnId": "col1",
            "isTransposed": false,
            "width": 200,
            "colorMode": "none"
          },
          {
            "columnId": "col2",
            "isTransposed": false,
            "colorMode": "cell",
            "palette": {
              "name": "custom",
              "type": "palette",
              "params": {
                "steps": 5,
                "stops": [
                  {"color": "#f7fbff", "stop": 0},
                  {"color": "#08519c", "stop": 100}
                ],
                "name": "custom",
                "colorStops": [],
                "rangeType": "number",
                "rangeMin": 0,
                "rangeMax": null
              }
            }
          },
          {
            "columnId": "col3",
            "isTransposed": false
          }
        ]
      }
    }
  },
  "references": [...]
}

COLOR MODES:
- "none": No coloring
- "cell": Color cell background
- "text": Color text only

PALETTE OPTIONS:
- Use "palette" for heatmap-style coloring
- Define color stops with min/max ranges
- "rangeType": "number" or "percent"
"""

LENS_METRIC_PROMPT = """
To create a Lens Metric (Single Number):

TYPE: "lens" with visualizationType: "lnsLegacyMetric" or "lnsMetric"

STRUCTURE:
{
  "attributes": {
    "title": "Metric Title",
    "visualizationType": "lnsLegacyMetric",
    "state": {
      "datasourceStates": {
        "formBased": {
          "layers": {
            "<layer-id>": {
              "columnOrder": ["col1"],
              "columns": {
                "col1": {
                  "label": "Average Price",
                  "dataType": "number",
                  "operationType": "average" | "sum" | "count" | "median" | "max" | "min",
                  "sourceField": "order.totalPrice",
                  "isBucketed": false,
                  "scale": "ratio",
                  "params": {
                    "format": {"id": "currency", "params": {"decimals": 2}}
                  }
                }
              },
              "incompleteColumns": {}
            }
          }
        }
      },
      "filters": [],
      "query": {"language": "kuery", "query": ""},
      "visualization": {
        "accessor": "col1",
        "layerId": "<layer-id>",
        "layerType": "data",
        "size": "xl" | "l" | "m" | "s",
        "textAlign": "center" | "left" | "right",
        "titlePosition": "bottom" | "top"
      }
    }
  },
  "references": [{
    "id": "<index-pattern-id>",
    "name": "indexpattern-datasource-current-indexpattern",
    "type": "index-pattern"
  }, {
    "id": "<index-pattern-id>",
    "name": "indexpattern-datasource-layer-<layer-id>",
    "type": "index-pattern"
  }]
}

SIZE OPTIONS:
- "xl": Extra large
- "l": Large
- "m": Medium
- "s": Small

TITLE POSITION:
- "bottom": Title below metric
- "top": Title above metric
"""

LENS_HEATMAP_PROMPT = """
To create a Lens Heatmap, use the following structure:

TYPE: "lnsXY" (Heatmaps are technically XY charts with specific configs)

1.  **datasourceStates**:
    -   **X-Axis**: Bucket (e.g., Time).
    -   **Y-Axis**: Bucket (e.g., Category).
    -   **Color**: Metric (e.g., Count).

2.  **visualization**:
    -   `layers`:
        -   `seriesType`: "heatmap" (or rely on grid config).
        -   `layerType`: "data".
        -   `xAccessor`: UUID of X bucket.
        -   `yAccessor`: UUID of Y bucket (This creates the grid).
        -   `colorAccessor`: UUID of Metric.
"""

LENS_PARTITION_PROMPT = """
To create a Lens Partition Chart (Treemap, Sunburst, Waffle), use the following structure:

IMPORTANT: Use visualizationType "lnsPie" with shape "treemap" (NOT "lnsPartition")

1.  **datasourceStates**:
    -   `formBased.layers`: Dictionary with layer IDs
    -   For each layer, define `columns`:
        -   **Buckets**: `operationType`: "terms" (for categorical grouping)
            -   `sourceField`: Field name (e.g., "category.keyword")
            -   `isBucketed`: true
            -   `scale`: "ordinal"
            -   `params`: {"size": 10, "orderBy": {"type": "column", "columnId": "metricId"}, "orderDirection": "desc"}
        -   **Metric**: `operationType`: "sum" | "count" | "average"
            -   `sourceField`: Field name (e.g., "taxful_total_price")
            -   `isBucketed`: false
            -   `scale`: "ratio"
            -   `params`: {"format": {"id": "currency", "params": {"decimals": 2}}}
    -   `columnOrder`: ["col1", "col2", "col3"]
    -   `indexPatternId`: "your-index-pattern-id" (REQUIRED - must match data view ID)

2.  **visualization**:
    -   `shape`: "treemap" | "sunburst" | "waffle" | "pie" | "donut"
    -   `layers`:
        -   `layerId`: Must match datasourceStates layer ID
        -   `primaryGroups`: ["col1", "col2"] (List of bucket column IDs in hierarchical order)
        -   `metrics`: ["col3"] (List of metric column IDs)
        -   `numberDisplay`: "percent" | "value"
        -   `categoryDisplay`: "default" | "hide"
        -   `legendDisplay`: "default" | "hide"
        -   `nestedLegend`: false
        -   `layerType`: "data"

3.  **references**: Array at root level (NOT in attributes)
    -   {"type": "index-pattern", "id": "index-pattern-id", "name": "indexpattern-datasource-layer-layerId"}

EXAMPLE COMPLETE PAYLOAD:
{
  "attributes": {
    "title": "Sales Treemap",
    "visualizationType": "lnsPie",
    "state": {
      "visualization": {
        "shape": "treemap",
        "layers": [{
          "layerId": "layer1",
          "primaryGroups": ["col1", "col2"],
          "metrics": ["col3"],
          "numberDisplay": "percent",
          "categoryDisplay": "default",
          "legendDisplay": "default",
          "nestedLegend": false,
          "layerType": "data"
        }]
      },
      "query": {"language": "kuery", "query": ""},
      "filters": [],
      "datasourceStates": {
        "formBased": {
          "layers": {
            "layer1": {
              "columnOrder": ["col1", "col2", "col3"],
              "columns": {
                "col1": {
                  "label": "Category",
                  "dataType": "string",
                  "operationType": "terms",
                  "sourceField": "category.keyword",
                  "isBucketed": true,
                  "scale": "ordinal",
                  "params": {"size": 10, "orderBy": {"type": "column", "columnId": "col3"}, "orderDirection": "desc"}
                },
                "col2": {
                  "label": "Manufacturer",
                  "dataType": "string",
                  "operationType": "terms",
                  "sourceField": "manufacturer.keyword",
                  "isBucketed": true,
                  "scale": "ordinal",
                  "params": {"size": 10, "orderBy": {"type": "column", "columnId": "col3"}, "orderDirection": "desc"}
                },
                "col3": {
                  "label": "Total Sales",
                  "dataType": "number",
                  "operationType": "sum",
                  "sourceField": "taxful_total_price",
                  "isBucketed": false,
                  "scale": "ratio",
                  "params": {"format": {"id": "currency", "params": {"decimals": 2}}}
                }
              },
              "indexPatternId": "kibana_sample_data_ecommerce"
            }
          }
        }
      }
    }
  },
  "references": [{
    "type": "index-pattern",
    "id": "kibana_sample_data_ecommerce",
    "name": "indexpattern-datasource-layer-layer1"
  }]
}
"""

LENS_MOSAIC_PROMPT = """
Lens Mosaic Chart:

NOTE: Mosaic visualization type not found in production instances.
Use lnsPie with shape "treemap" for similar hierarchical proportional visualization.

For mosaic-like visualizations, consider:
1. Treemap (lnsPie with shape: "treemap")
2. Heatmap (lnsXY with appropriate configuration)
3. Waffle chart (lnsPie with shape: "waffle")

See lens_pie prompt for treemap implementation.
"""

LENS_TAG_CLOUD_PROMPT = """
Lens Tag Cloud:

NOTE: Tag cloud not found as native Lens type in production instances.
Tag clouds are legacy visualizations.

For word/term frequency visualization, use:
1. Bar chart (lnsXY) with terms aggregation
2. Pie chart (lnsPie) for top terms
3. Data table (lnsDatatable) for detailed term lists

See lens_xy or lens_pie prompts for implementation.
"""

LENS_PROMPTS = {
    "lens_xy": LENS_XY_PROMPT,
    "lens_pie": LENS_PIE_PROMPT,
    "lens_datatable": LENS_DATATABLE_PROMPT,
    "lens_metric": LENS_METRIC_PROMPT,
    "lens_heatmap": LENS_HEATMAP_PROMPT,
    "lens_partition": LENS_PARTITION_PROMPT,
    "lens_mosaic": LENS_MOSAIC_PROMPT,
    "lens_tag_cloud": LENS_TAG_CLOUD_PROMPT
}
