"""
General Guidelines for Kibana Saved Objects
"""

GENERAL_GUIDELINES_PROMPT = """
# General Guidelines for Creating Kibana Saved Objects

## CRITICAL RULES FOR PRODUCTION

1. **Type-Specific Saved Object Structure**:
   - TYPE "lens": Modern visualizations (XY, Pie, Treemap, etc.)
   - TYPE "visualization": Legacy visualizations (Vega, Markdown, TSVB, Input Controls)
   - TYPE "dashboard": Dashboard containers
   - TYPE "index-pattern": Data views (deprecated, use data_view API)

2. **References Array (CRITICAL)**:
   - ALWAYS include references array at ROOT level (not in attributes)
   - Format: [{"type": "index-pattern", "id": "<uuid>", "name": "<ref-name>"}]
   - Common reference names:
     * "indexpattern-datasource-current-indexpattern"
     * "indexpattern-datasource-layer-<layer-id>"
     * "control_0_index_pattern" (for input controls)
     * "kibanaSavedObjectMeta.searchSourceJSON.index"

3. **Stringified JSON Fields**:
   - visState: MUST be stringified JSON string, not object
   - uiStateJSON: MUST be stringified JSON string
   - searchSourceJSON: MUST be stringified JSON string
   - Example: "visState": "{\"title\":\"Chart\",\"type\":\"vega\"}"

4. **Lens Visualizations Structure**:
   ```json
   {
     "attributes": {
       "title": "Chart Title",
       "visualizationType": "lnsXY" | "lnsPie" | "lnsDatatable" | "lnsMetric",
       "state": {
         "datasourceStates": {
           "formBased": {
             "layers": {
               "<layer-id>": {
                 "columnOrder": ["col1", "col2"],
                 "columns": { ... },
                 "indexPatternId": "<index-pattern-id>"
               }
             }
           }
         },
         "visualization": { ... },
         "query": {"language": "kuery", "query": ""},
         "filters": []
       }
     },
     "references": [...]
   }
   ```

5. **Legacy Visualization Structure**:
   ```json
   {
     "attributes": {
       "title": "Viz Title",
       "visState": "{\"title\":\"...\",\"type\":\"vega\",\"params\":{...},\"aggs\":[]}",
       "uiStateJSON": "{}",
       "description": "",
       "version": 1,
       "kibanaSavedObjectMeta": {
         "searchSourceJSON": "{\"query\":{\"query\":\"\",\"language\":\"kuery\"},\"filter\":[]}"
       }
     },
     "references": [...]
   }
   ```

6. **Column IDs and Layer IDs**:
   - Use simple strings: "col1", "col2", "layer1"
   - OR use UUIDs: "a8511a62-2b78-4ba4-9425-a417df6e059f"
   - Be consistent within a single visualization
   - columnOrder must list ALL column IDs in order

7. **Field Types**:
   - Keyword fields: Use for terms aggregations (e.g., "category.keyword")
   - Numeric fields: Use for metrics and range aggregations
   - Date fields: Use for date_histogram
   - Geo fields: Use for geospatial visualizations

8. **Common Mistakes to Avoid**:
   - ❌ Forgetting to stringify visState/uiStateJSON
   - ❌ Missing references array
   - ❌ Wrong reference name format
   - ❌ Using non-keyword fields for terms aggregation
   - ❌ Missing indexPatternId in Lens layers
   - ❌ Inconsistent column IDs between datasourceStates and visualization

9. **Format Specifications**:
   - Currency: {"id": "currency", "params": {"decimals": 2}}
   - Percent: {"id": "percent", "params": {"decimals": 1}}
   - Number: {"id": "number", "params": {"decimals": 0}}
   - Bytes: {"id": "bytes", "params": {"decimals": 2}}

10. **Migration Versions** (Optional but recommended):
    - lens: "10.1.0"
    - visualization: "8.5.0"
    - coreMigrationVersion: "8.8.0"
    - typeMigrationVersion: "10.1.0" (for lens) or "8.5.0" (for visualization)

## WORKFLOW FOR CREATING VISUALIZATIONS

1. Get available data views: `get_all_data_views()`
2. Choose appropriate visualization type
3. Get instructions: `get_visualization_instructions(key)`
4. Build payload following the exact structure
5. Create: `create_saved_object(type, attributes, references)`

## TESTING CHECKLIST

Before creating a saved object, verify:
- [ ] Type is correct ("lens" or "visualization")
- [ ] References array exists at root level
- [ ] Reference names match usage in attributes
- [ ] visState/uiStateJSON are stringified (if applicable)
- [ ] indexPatternId matches reference id (for Lens)
- [ ] Field names exist in the data view
- [ ] Column IDs are consistent throughout
"""

GENERAL_GUIDELINES = {
    "general": GENERAL_GUIDELINES_PROMPT
}
