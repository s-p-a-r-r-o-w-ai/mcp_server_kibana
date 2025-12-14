"""
Vega Visualization Prompts
Instructions for creating highly custom visualizations using Vega within Kibana.
"""

VEGA_PROMPT = """
To create a Vega/Vega-Lite visualization in Kibana:

TYPE: "visualization" with visState.type: "vega"

CRITICAL STRUCTURE:
{
  "attributes": {
    "title": "Visualization Title",
    "visState": "{\"title\":\"Title\",\"type\":\"vega\",\"aggs\":[],\"params\":{\"spec\":\"{...vega-spec...}\"}}",
    "uiStateJSON": "{}",
    "description": "",
    "version": 1,
    "kibanaSavedObjectMeta": {
      "searchSourceJSON": "{\"query\":{\"query\":\"\",\"language\":\"kuery\"},\"filter\":[]}"
    }
  },
  "references": []  // Add index-pattern reference if needed
}

VEGA v5 SPEC (Full Vega - for complex visualizations):
{
  "$schema": "https://vega.github.io/schema/vega/v5.json",
  "config": {
    "kibana": {"type": "map", "latitude": 25, "longitude": -40, "zoom": 3}
  },
  "data": [{
    "name": "table",
    "url": {
      "index": "kibana_sample_data_logs",
      "%context%": true,
      "%timefield%": "timestamp",
      "body": {
        "size": 0,
        "aggs": {
          "gridSplit": {
            "geotile_grid": {"field": "geo.coordinates", "precision": 5, "size": 10000},
            "aggs": {
              "gridCentroid": {
                "geo_centroid": {"field": "geo.coordinates"}
              }
            }
          }
        }
      }
    },
    "format": {"property": "aggregations.gridSplit.buckets"},
    "transform": [{
      "type": "geopoint",
      "projection": "projection",
      "fields": ["gridCentroid.location.lon", "gridCentroid.location.lat"]
    }]
  }],
  "scales": [{
    "name": "gridSize",
    "type": "linear",
    "domain": {"data": "table", "field": "doc_count"},
    "range": [50, 1000]
  }],
  "marks": [{
    "name": "gridMarker",
    "type": "symbol",
    "from": {"data": "table"},
    "encode": {
      "update": {
        "size": {"scale": "gridSize", "field": "doc_count"},
        "xc": {"signal": "datum.x"},
        "yc": {"signal": "datum.y"},
        "tooltip": {"signal": "{count: datum.doc_count}"}
      }
    }
  }]
}

VEGA-LITE v5 SPEC (Simpler syntax for standard charts):
{
  "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
  "data": {
    "url": {
      "%context%": true,
      "%timefield%": "@timestamp",
      "index": "kibana_sample_data_logs",
      "body": {
        "aggs": {
          "countries": {
            "terms": {"field": "geo.dest", "size": 25},
            "aggs": {
              "hours": {
                "histogram": {"field": "hour_of_day", "interval": 1},
                "aggs": {
                  "unique": {"cardinality": {"field": "clientip"}}
                }
              }
            }
          }
        },
        "size": 0
      }
    },
    "format": {"property": "aggregations.countries.buckets"}
  },
  "transform": [
    {"flatten": ["hours.buckets"], "as": ["buckets"]},
    {"filter": "datum.buckets.unique.value > 0"}
  ],
  "mark": {"type": "rect", "tooltip": true},
  "encoding": {
    "x": {
      "field": "buckets.key",
      "type": "nominal",
      "axis": {"title": "Hour", "labelAngle": 0}
    },
    "y": {
      "field": "key",
      "type": "nominal",
      "axis": {"title": "Country"}
    },
    "color": {
      "field": "buckets.unique.value",
      "type": "quantitative",
      "scale": {"scheme": "blues"}
    }
  }
}

KEY FEATURES:
1. **Kibana Context**: %context%: true respects time picker and filters
2. **Map Support**: config.kibana for map-based visualizations
3. **ES Aggregations**: Full ES DSL query support in body
4. **Transforms**: geopoint, formula, filter, flatten for data manipulation
5. **Interactivity**: Signals, tooltips, hover effects

COMMON USE CASES:
- Geospatial maps with custom markers
- Sankey diagrams for flow visualization
- Heatmaps with custom color schemes
- Network graphs and connections
- Custom chart types not available in Lens
"""

VEGA_PROMPTS = {
    "vega_general": VEGA_PROMPT
}
