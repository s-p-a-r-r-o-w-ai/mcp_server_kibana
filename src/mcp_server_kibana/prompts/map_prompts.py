"""
Map Visualization Prompts
Instructions for creating Kibana Maps (Saved Object type: "map").
"""

MAP_PROMPT = """
To create a Kibana Map, the critical attribute is `layerListJSON` (stringified JSON).

TYPE: "map"

Attributes Structure:
- `title`: Map Title.
- `mapStateJSON`: { "zoom": 2, "center": { "lat": 0, "lon": 0 }, "timeFilters": ... }
- `layerListJSON`: ARRAY of Layer Objects.

LAYER TYPES & CONFIGURATION:

1.  **EMS Vector Layer (Background/Regions)**:
    -   `type`: "EMS_FILE" or "EMS_VECTOR_TILE".
    -   `sourceDescriptor`: { "type": "EMS_FILE", "id": "world_countries" }.
    -   **Choropleth (Join)**: To color regions by data:
        -   `joins`: [
            {
                "leftField": "iso2" (Field in EMS file),
                "right": {
                    "type": "ES_TERM_SOURCE",
                    "indexPatternTitle": "my-index",
                    "term": "geoip.country_iso_code" (Field in Index),
                    "metrics": [ { "type": "count", "label": "Count" } ]
                }
            }
        ]
    -   **Style**: Use `fillColor` with `type`: "DYNAMIC" mapped to the metric (e.g., `__kbnjoin__count__...`).

2.  **Grid Aggregation Layer (Heatmap/Clusters)**:
    -   `type`: "GEOJSON_VECTOR".
    -   `sourceDescriptor`: {
            "type": "ES_GEO_GRID",
            "resolution": "COARSE",
            "geoField": "geo.coordinates",
            "requestType": "point",
            "metrics": [{ "type": "sum", "field": "sales" }]
        }
    -   **Style**:
        -   `fillColor`: Dynamic based on metric.
        -   `iconSize`: Dynamic based on metric.

3.  **Document Layer (Points)**:
    -   `type`: "GEOJSON_VECTOR" (or "MVT_VECTOR" for large data).
    -   `sourceDescriptor`: {
            "type": "ES_SEARCH",
            "geoField": "geo.coordinates",
            "limit": 1000,
            "filterByMapBounds": true
        }

KEY TIP: Always ensure `indexPatternRefName` in the layer config matches a reference in the Saved Object `references` array.
"""

MAP_PROMPTS = {
    "map_general": MAP_PROMPT
}
