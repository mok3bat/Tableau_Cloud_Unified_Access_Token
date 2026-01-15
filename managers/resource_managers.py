"""Resource manager classes for different Tableau resources."""


# --- Resource Manager class for Projects, Workbooks, Datasources, Flows ---
class ResourceManager:
    """Manages Tableau site configurations."""
    def __init__(self, resource_type):
        self.resource_type = resource_type  # 'project', 'workbook', 'datasource', 'flow'
        self.resources = []
    
    def add_resource(self, luid, scope):
        """Add a new resource"""
        if not luid:
            return self.get_display(), self.get_choices(), f"Please enter {self.resource_type.title()} LUID"
        
        # Check for duplicates
        for res in self.resources:
            if res["luid"] == luid:
                return self.get_display(), self.get_choices(), f"{self.resource_type.title()} '{luid}' already exists"
        
        self.resources.append({"luid": luid, "scope": scope})
        return self.get_display(), self.get_choices(), f"Added {self.resource_type}: {luid}"
    
    def delete_resource(self, luid):
        """Delete selected resource"""
        if luid:
            self.resources = [r for r in self.resources if r["luid"] != luid]
        return self.get_display(), self.get_choices(), f"Deleted {self.resource_type}: {luid}"
    
    def clear_resources(self):
        """Clear all resources"""
        self.resources = []
        return self.get_display(), self.get_choices(), f"All {self.resource_type}s cleared"
    
    def get_display(self):
        """Create HTML display"""
        if not self.resources:
            return f"<div style='padding: 15px; background: #f8f9fa; border-radius: 8px; border: 2px dashed #dee2e6; text-align: center; color: #6c757d; font-style: italic;'>No {self.resource_type}s configured yet</div>"
        
        html = """
        <div style='padding: 15px; background: #f8f9fa; border-radius: 8px; border: 1px solid #dee2e6;'>
            <div style='display: flex; align-items: center; margin-bottom: 12px; padding-bottom: 10px; border-bottom: 2px solid #adb5bd;'>
                <div style='flex: 3; font-weight: bold; color: #495057; font-size: 0.95em;'>LUID</div>
                <div style='flex: 2; font-weight: bold; color: #495057; font-size: 0.95em;'>SCOPE</div>
            </div>
        """
        
        for idx, res in enumerate(self.resources):
            bg_color = '#ffffff' if idx % 2 == 0 else '#f8f9fa'
            html += f"""
            <div style='display: flex; align-items: center; margin: 8px 0; padding: 12px; 
                        border-left: 3px solid #0d6efd; border-radius: 4px; 
                        background: {bg_color}; transition: all 0.2s;
                        box-shadow: 0 1px 3px rgba(0,0,0,0.05);'
                 onmouseover="this.style.backgroundColor='#e7f1ff'" 
                 onmouseout="this.style.backgroundColor='{bg_color}'">
                
                <div style='flex: 3; padding-right: 15px;'>
                    <div style='font-family: monospace; color: #495057; font-size: 0.85em;'>{res['luid']}</div>
                </div>
                
                <div style='flex: 2;'>
                    <div style='color: #6c757d; font-size: 0.85em;'>{res['scope']}</div>
                </div>
            </div>
            """
        
        html += f"""
            <div style='margin-top: 12px; padding-top: 10px; border-top: 1px solid #dee2e6; 
                        color: #6c757d; font-size: 0.85em; text-align: right;'>
                Total: {len(self.resources)}
            </div>
        </div>
        """
        return html
    
    def get_choices(self):
        """Get LUIDs for radio selection"""
        return [res["luid"] for res in self.resources]
    
    def get_resources_list(self):
        """Get list of resources"""
        return self.resources