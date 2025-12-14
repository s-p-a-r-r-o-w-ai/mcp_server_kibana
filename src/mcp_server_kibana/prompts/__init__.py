from .lens_prompts import LENS_PROMPTS
from .map_prompts import MAP_PROMPTS
from .vega_prompts import VEGA_PROMPTS
from .dashboard_prompts import DASHBOARD_PROMPTS
from .general_guidelines import GENERAL_GUIDELINES

# Aggregate all prompts into a single dictionary
KIBANA_PROMPTS = {
    **LENS_PROMPTS,
    **MAP_PROMPTS,
    **VEGA_PROMPTS,
    **DASHBOARD_PROMPTS,
    **GENERAL_GUIDELINES
}
