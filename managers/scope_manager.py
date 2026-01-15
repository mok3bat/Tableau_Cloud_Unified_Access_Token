"""Scope management for JWT tokens."""

import pandas as pd
from scope_data import SCOPE_DEFINITIONS, COMMON_ACTIONS


# --- ScopeManager class using radio button approach ---
class ScopeManager:
    def __init__(self):
        self.scopes = []  # List of dictionaries with "Scope" and "Description"
    
    def add_scope(self, resource, action):
        """Add a new scope with resource and action"""
        if not resource or not action:
            return self.get_form_display(), self.get_radio_choices(), "Please select both a resource and an action."
        
        prefix = SCOPE_DEFINITIONS.get(resource, {}).get("prefix", f"tableau:{resource}")
        new_scope = f"{prefix}:{action}"
        description = SCOPE_DEFINITIONS.get(resource, {}).get("description", "N/A")
        
        # Check for duplicates
        for scope_dict in self.scopes:
            if scope_dict["Scope"] == new_scope:
                return self.get_form_display(), self.get_radio_choices(), f"Scope '{new_scope}' already exists."
        
        self.scopes.append({"Scope": new_scope, "Description": description})
        return self.get_form_display(), self.get_radio_choices(), f"Added: {new_scope}"
    
    def delete_scope(self, selected_scope):
        """Delete selected scope"""
        if selected_scope:
            # Find and remove the scope
            self.scopes = [s for s in self.scopes if s["Scope"] != selected_scope]
        return self.get_form_display(), self.get_radio_choices(), f"Deleted: {selected_scope}"
    
    def clear_scopes(self):
        """Clear all scopes"""
        self.scopes = []
        return self.get_form_display(), self.get_radio_choices(), "All scopes cleared."
    
    def get_form_display(self):
        """Create improved HTML display of current scopes"""
        if not self.scopes:
            return """
            <div style='padding: 20px; color: #666; font-style: italic; text-align: center; 
                        background: #f8f9fa; border-radius: 8px; border: 2px dashed #dee2e6;'>
                No scopes selected yet. Add scopes using the controls above.
            </div>
            """
        
        html = """
        <div style='padding: 15px; background: #f8f9fa; border-radius: 8px; border: 1px solid #dee2e6;'>
            <div style='display: flex; align-items: center; margin-bottom: 12px; padding-bottom: 10px; 
                        border-bottom: 2px solid #adb5bd;'>
                <div style='flex: 2; font-weight: bold; color: #495057; font-size: 0.95em;'>SCOPE</div>
                <div style='flex: 3; font-weight: bold; color: #495057; font-size: 0.95em;'>DESCRIPTION</div>
            </div>
        """
        
        for idx, scope_dict in enumerate(self.scopes):
            # Alternate row colors for better readability
            bg_color = '#ffffff' if idx % 2 == 0 else '#f8f9fa'
            
            html += f"""
            <div style='display: flex; align-items: center; margin: 8px 0; padding: 12px; 
                        border-left: 3px solid #0d6efd; border-radius: 4px; 
                        background: {bg_color}; transition: all 0.2s;
                        box-shadow: 0 1px 3px rgba(0,0,0,0.05);'
                 onmouseover="this.style.backgroundColor='#e7f1ff'; this.style.boxShadow='0 2px 5px rgba(0,0,0,0.1)'" 
                 onmouseout="this.style.backgroundColor='{bg_color}'; this.style.boxShadow='0 1px 3px rgba(0,0,0,0.05)'">
                
                <div style='flex: 2; padding-right: 15px;'>
                    <div style='font-weight: 500; color: #212529; font-family: monospace; font-size: 0.9em;'>
                        {scope_dict['Scope']}
                    </div>
                </div>
                
                <div style='flex: 3; padding-left: 15px;'>
                    <div style='color: #6c757d; font-size: 0.9em; line-height: 1.4;'>
                        {scope_dict['Description']}
                    </div>
                </div>
            </div>
            """
        
        html += """
            <div style='margin-top: 12px; padding-top: 10px; border-top: 1px solid #dee2e6; 
                        color: #6c757d; font-size: 0.85em; text-align: right;'>
                Total scopes: """ + str(len(self.scopes)) + """
            </div>
        </div>
        """
        return html
    
    def get_radio_choices(self):
        """Get choices for radio button selection"""
        return [scope_dict["Scope"] for scope_dict in self.scopes]
    
    def get_scopes_df(self):
        """Convert to DataFrame for compatibility with existing code"""
        if not self.scopes:
            return pd.DataFrame(columns=["Scope", "Description"])
        return pd.DataFrame(self.scopes)