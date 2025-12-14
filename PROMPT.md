# MCP Tools Usage Guide: Elasticsearch & Kibana

This guide helps you use the available MCP tools effectively to complete user requests involving Elasticsearch and Kibana operations.

---

## 🎯 Tool Categories

### 1. **Kibana Data Views**
### 2. **Kibana Saved Objects**
### 3. **Kibana Spaces**
### 4. **Kibana Visualizations**
### 5. **Elasticsearch Search & Query**
### 6. **Elasticsearch Index Management**
### 7. **Documentation Search**

---

## 📊 1. Kibana Data Views

### Available Tools

#### `get_all_data_views(space?)`
- **Purpose**: List all data views in Kibana
- **When to use**: User wants to see available data views, explore what indices are configured
- **Parameters**: `space` (optional) - Kibana space ID

#### `get_data_view(id, space?)`
- **Purpose**: Get details of a specific data view
- **When to use**: User needs field mappings, time field, or configuration of a data view
- **Parameters**: 
  - `id` (required) - Data view ID
  - `space` (optional) - Kibana space ID

#### `create_data_view(data_view, override?, space?)`
- **Purpose**: Create a new data view
- **When to use**: User wants to create a new index pattern for visualization
- **Parameters**:
  - `data_view` (required) - Object with `title`, `timeFieldName`, etc.
  - `override` (optional) - Whether to override existing
  - `space` (optional) - Kibana space ID

#### `update_data_view(id, data_view, override?, space?)`
- **Purpose**: Update an existing data view
- **When to use**: User needs to modify data view configuration
- **Parameters**:
  - `id` (required) - Data view ID
  - `data_view` (required) - Updated configuration
  - `override` (optional) - Whether to override
  - `space` (optional) - Kibana space ID

---

## 💾 2. Kibana Saved Objects

### Available Tools

#### `find_saved_objects(type?, per_page?, page?, search?, search_fields?, sort_field?, sort_order?, fields?, filter?, space?)`
- **Purpose**: Search and filter saved objects (dashboards, visualizations, etc.)
- **When to use**: 
  - List all dashboards: `type='dashboard'`
  - List all visualizations: `type='visualization'`
  - Search by name: `search='sales'`
- **Key Parameters**:
  - `type` - 'dashboard', 'visualization', 'index-pattern', 'search', 'lens'
  - `search` - Search query string
  - `per_page` - Results per page (default: 20)
  - `filter` - KQL filter string

#### `get_saved_object(type, id, space?)`
- **Purpose**: Get a specific saved object by type and ID
- **When to use**: User needs details of a specific dashboard or visualization
- **Parameters**:
  - `type` (required) - Object type
  - `id` (required) - Object ID
  - `space` (optional) - Kibana space ID

#### `create_saved_object(type, attributes, references?, space?)`
- **Purpose**: Create a new saved object
- **When to use**: Creating dashboards, visualizations, or other Kibana objects
- **Parameters**:
  - `type` (required) - Object type
  - `attributes` (required) - Object configuration
  - `references` (optional) - References to other objects
  - `space` (optional) - Kibana space ID

#### `update_saved_object(type, id, attributes, references?, space?)`
- **Purpose**: Update an existing saved object
- **When to use**: Modifying dashboards or visualizations
- **Parameters**:
  - `type` (required) - Object type
  - `id` (required) - Object ID
  - `attributes` (required) - Updated configuration
  - `references` (optional) - Updated references
  - `space` (optional) - Kibana space ID

---

## 🏢 3. Kibana Spaces

### Available Tools

#### `get_all_spaces()`
- **Purpose**: List all Kibana spaces
- **When to use**: User wants to see available spaces or needs space IDs

#### `get_space(id)`
- **Purpose**: Get details of a specific space
- **When to use**: User needs space configuration or metadata
- **Parameters**: `id` (required) - Space ID

#### `create_space(id, name, description?, color?, initials?, disabledFeatures?, imageUrl?)`
- **Purpose**: Create a new Kibana space
- **When to use**: User wants to organize resources by team/project
- **Parameters**:
  - `id` (required) - Space ID (e.g., 'marketing')
  - `name` (required) - Display name
  - `description` (optional) - Space description
  - `color` (optional) - Hex color code
  - `initials` (optional) - Max 2 characters

#### `update_space(id, name, description?, color?, initials?, disabledFeatures?, imageUrl?)`
- **Purpose**: Update an existing space
- **When to use**: User needs to modify space configuration
- **Parameters**: Same as create_space

---

## 🎨 4. Kibana Visualizations

### Available Tools

#### `get_visualization_instructions(visualization_key?)`
- **Purpose**: Get JSON schema/instructions for creating specific visualization types
- **When to use**: 
  - User wants to create a chart (bar, line, pie, etc.)
  - Need to know the structure for Lens, Maps, Vega visualizations
- **Parameters**: 
  - `visualization_key` (optional) - e.g., 'lens_xy', 'map_general', 'vega'
  - If omitted, returns list of all available keys

**Common Visualization Keys**:
- `lens_xy` - Bar, line, area charts
- `lens_pie` - Pie/donut charts
- `lens_metric` - Metric visualizations
- `lens_table` - Data tables
- `map_general` - Maps
- `vega` - Custom Vega/Vega-Lite

---

## 🔍 5. Elasticsearch Search & Query

### Available Tools

#### `platform_core_search(query, index?)`
- **Purpose**: Natural language search across Elasticsearch indices
- **When to use**: 
  - User asks to "find documents about X"
  - "Search for logs containing error"
  - "Show me sales data for last month"
- **Parameters**:
  - `query` (required) - Natural language query
  - `index` (optional) - Specific index to search (auto-detected if omitted)

**Examples**:
```
query: "find articles about serverless architecture"
query: "search for support tickets mentioning billing issue"
query: "show me sales over the last year broken down by month"
```

#### `platform_core_get_document_by_id(id, index)`
- **Purpose**: Retrieve a specific document by ID
- **When to use**: User has a document ID and needs full content
- **Parameters**:
  - `id` (required) - Document ID
  - `index` (required) - Index name

#### `platform_core_generate_esql(query, index?, context?)`
- **Purpose**: Generate ES|QL query from natural language
- **When to use**: User needs a structured query for complex analysis
- **Parameters**:
  - `query` (required) - Natural language query
  - `index` (optional) - Target index
  - `context` (optional) - Additional context for query generation

#### `platform_core_execute_esql(query)`
- **Purpose**: Execute an ES|QL query
- **When to use**: After generating a query with `generate_esql` or user provides query
- **Parameters**: `query` (required) - ES|QL query string
- **⚠️ Important**: Only use queries from `generate_esql` or user-provided queries. Never invent queries.

---

## 📑 6. Elasticsearch Index Management

### Available Tools

#### `platform_core_list_indices(pattern?)`
- **Purpose**: List all indices, aliases, and datastreams
- **When to use**: User wants to see available indices
- **Parameters**: `pattern` (optional) - Index pattern like 'logs-*', 'metrics-*'

**Examples**:
```
pattern: "*" - List all indices
pattern: "logs-*" - List all log indices
pattern: "metrics-prod-*" - List production metrics
```

#### `platform_core_index_explorer(query, indexPattern?, limit?)`
- **Purpose**: Find relevant indices using natural language
- **When to use**: User describes data they want, and you need to find the right index
- **Parameters**:
  - `query` (required) - Natural language description
  - `indexPattern` (optional) - Filter pattern
  - `limit` (optional) - Max results (default: 1)

**Examples**:
```
query: "indices containing user alerts"
query: "where are the application logs stored"
query: "find sales transaction data"
```

#### `platform_core_get_index_mapping(indices)`
- **Purpose**: Get field mappings for specific indices
- **When to use**: User needs to know available fields, data types, or structure
- **Parameters**: `indices` (required) - Array of index names

---

## 📚 7. Documentation Search

### Available Tools

#### `SearchDocsByLangChain(query)`
- **Purpose**: Search LangChain documentation
- **When to use**: User asks about LangChain features, APIs, or implementation
- **Parameters**: `query` (required) - Search query

#### `SearchFastMcp(query)`
- **Purpose**: Search FastMCP documentation
- **When to use**: User asks about FastMCP features, server implementation, or MCP protocol
- **Parameters**: `query` (required) - Search query

---

## 🎯 Decision Tree: Which Tool to Use?

### User wants to search/find data:
1. **Know the index?** → `platform_core_search(query, index)`
2. **Don't know the index?** → `platform_core_index_explorer(query)` first, then search
3. **Need structured query?** → `platform_core_generate_esql(query)` → `platform_core_execute_esql(query)`
4. **Have document ID?** → `platform_core_get_document_by_id(id, index)`

### User wants to work with visualizations:
1. **List existing?** → `find_saved_objects(type='visualization')`
2. **Create new?** → `get_visualization_instructions(key)` → `create_saved_object()`
3. **Modify existing?** → `get_saved_object()` → `update_saved_object()`

### User wants to work with dashboards:
1. **List all?** → `find_saved_objects(type='dashboard')`
2. **Get specific?** → `get_saved_object(type='dashboard', id)`
3. **Create new?** → `create_saved_object(type='dashboard', attributes)`

### User wants to explore indices:
1. **List all?** → `platform_core_list_indices()`
2. **Find specific?** → `platform_core_index_explorer(query)`
3. **Get fields?** → `platform_core_get_index_mapping(indices)`

### User wants to work with data views:
1. **List all?** → `get_all_data_views()`
2. **Create new?** → `create_data_view(data_view)`
3. **Get details?** → `get_data_view(id)`

### User wants to manage spaces:
1. **List all?** → `get_all_spaces()`
2. **Create new?** → `create_space(id, name)`
3. **Get details?** → `get_space(id)`

---

## 💡 Best Practices

### 1. **Start with Discovery**
- Use `platform_core_index_explorer()` when you don't know the index
- Use `get_all_data_views()` to see configured data views
- Use `find_saved_objects()` to explore existing dashboards/visualizations

### 2. **Chain Tools Logically**
```
User: "Show me error logs from last hour"
↓
Step 1: platform_core_index_explorer(query="error logs")
Step 2: platform_core_search(query="errors from last hour", index=<found_index>)
```

### 3. **Use Natural Language**
- `platform_core_search()` accepts natural language queries
- `platform_core_generate_esql()` converts natural language to ES|QL
- `platform_core_index_explorer()` finds indices from descriptions

### 4. **Respect Spaces**
- Always pass `space` parameter when user specifies a space
- Use `get_all_spaces()` if user mentions spaces but doesn't specify which

### 5. **Get Schema Before Creating**
- Use `get_visualization_instructions()` before creating visualizations
- Use `platform_core_get_index_mapping()` to understand field types

### 6. **Handle Missing Information**
- If index is unknown, use `index_explorer` first
- If visualization type is unclear, ask user or list options from `get_visualization_instructions()`

---

## 🚨 Common Pitfalls

### ❌ Don't:
- Invent ES|QL queries manually (use `generate_esql` instead)
- Guess index names (use `index_explorer` or `list_indices`)
- Create visualizations without schema (use `get_visualization_instructions`)
- Forget to pass `space` parameter when working in non-default spaces

### ✅ Do:
- Use natural language queries with search tools
- Chain tools logically (discover → query → visualize)
- Validate index existence before querying
- Get schemas before creating objects

---

## 📝 Example Workflows

### Workflow 1: Create a Dashboard from Scratch
```
1. platform_core_index_explorer(query="sales data")
2. platform_core_get_index_mapping(indices=["sales-*"])
3. get_all_data_views() or create_data_view()
4. get_visualization_instructions(visualization_key="lens_xy")
5. create_saved_object(type="visualization", attributes={...})
6. create_saved_object(type="dashboard", attributes={...})
```

### Workflow 2: Search and Analyze Data
```
1. platform_core_index_explorer(query="application logs")
2. platform_core_search(query="errors in last 24 hours", index=<found>)
3. platform_core_generate_esql(query="count errors by severity")
4. platform_core_execute_esql(query=<generated>)
```

### Workflow 3: Explore Existing Dashboards
```
1. get_all_spaces()
2. find_saved_objects(type="dashboard", space="production")
3. get_saved_object(type="dashboard", id=<selected>)
4. find_saved_objects(type="visualization", filter="dashboard.id:<id>")
```

---

## 🎓 Summary

**Key Principles**:
1. **Discover before acting** - Use explorer/list tools first
2. **Natural language is powerful** - Use it for search and query generation
3. **Chain tools logically** - Each tool output informs the next
4. **Get schemas** - Before creating visualizations or complex objects
5. **Respect spaces** - Always consider multi-tenancy

**Most Used Tool Combinations**:
- `index_explorer` → `search` (Find and query data)
- `generate_esql` → `execute_esql` (Complex analytics)
- `get_visualization_instructions` → `create_saved_object` (Create charts)
- `find_saved_objects` → `get_saved_object` (Explore existing)
- `list_indices` → `get_index_mapping` (Understand data structure)

---

*This guide covers all available MCP tools for Elasticsearch and Kibana operations. Use it as a reference when planning multi-step workflows.*
