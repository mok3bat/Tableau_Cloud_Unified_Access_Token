"""Scope management for JWT tokens."""

# --- Site Manager class ---
class SiteManager:
    def __init__(self):
        self.sites = []  # List of dictionaries with site info
    
    def add_site(self, site_id, site_luid, site_scope):
        """Add a new site"""
        if not site_id or not site_luid:
            return self.get_sites_display(), self.get_site_choices(), "Please enter both Site ID and Site LUID"
        
        # Check for duplicates
        for site in self.sites:
            if site["site_id"] == site_id or site["site_luid"] == site_luid:
                return self.get_sites_display(), self.get_site_choices(), f"Site '{site_id}' already exists"
        
        self.sites.append({
            "site_id": site_id,
            "site_luid": site_luid,
            "scope": site_scope
        })
        
        return self.get_sites_display(), self.get_site_choices(), f"Added site: {site_id}"
    
    def delete_site(self, site_key):
        """Delete selected site by key (site_id)"""
        if site_key:
            self.sites = [s for s in self.sites if s["site_id"] != site_key]
        return self.get_sites_display(), self.get_site_choices(), f"Deleted site: {site_key}"
    
    def clear_sites(self):
        """Clear all sites"""
        self.sites = []
        return self.get_sites_display(), self.get_site_choices(), "All sites cleared"
    
    def get_sites_display(self):
        """Create HTML display of sites"""
        if not self.sites:
            return "<div style='padding: 15px; background: #f8f9fa; border-radius: 8px; border: 2px dashed #dee2e6; text-align: center; color: #6c757d; font-style: italic;'>No sites configured yet</div>"
        
        html = """
        <div style='padding: 15px; background: #f8f9fa; border-radius: 8px; border: 1px solid #dee2e6;'>
            <div style='display: flex; align-items: center; margin-bottom: 12px; padding-bottom: 10px; border-bottom: 2px solid #adb5bd;'>
                <div style='flex: 2; font-weight: bold; color: #495057; font-size: 0.95em;'>SITE ID</div>
                <div style='flex: 3; font-weight: bold; color: #495057; font-size: 0.95em;'>SITE LUID</div>
                <div style='flex: 2; font-weight: bold; color: #495057; font-size: 0.95em;'>SCOPE</div>
            </div>
        """
        
        for idx, site in enumerate(self.sites):
            bg_color = '#ffffff' if idx % 2 == 0 else '#f8f9fa'
            html += f"""
            <div style='display: flex; align-items: center; margin: 8px 0; padding: 12px; 
                        border-left: 3px solid #0d6efd; border-radius: 4px; 
                        background: {bg_color}; transition: all 0.2s;
                        box-shadow: 0 1px 3px rgba(0,0,0,0.05);'
                 onmouseover="this.style.backgroundColor='#e7f1ff'" 
                 onmouseout="this.style.backgroundColor='{bg_color}'">
                
                <div style='flex: 2; padding-right: 15px;'>
                    <div style='font-weight: 500; color: #212529;'>{site['site_id']}</div>
                </div>
                
                <div style='flex: 3; padding-right: 15px;'>
                    <div style='font-family: monospace; color: #495057; font-size: 0.85em;'>{site['site_luid']}</div>
                </div>
                
                <div style='flex: 2;'>
                    <div style='color: #6c757d; font-size: 0.85em;'>{site['scope']}</div>
                </div>
            </div>
            """
        
        html += f"""
            <div style='margin-top: 12px; padding-top: 10px; border-top: 1px solid #dee2e6; 
                        color: #6c757d; font-size: 0.85em; text-align: right;'>
                Total sites: {len(self.sites)}
            </div>
        </div>
        """
        return html
    
    def get_site_choices(self):
        """Get site IDs for radio selection"""
        return [site["site_id"] for site in self.sites]
    
    def get_sites_list(self):
        """Get list of sites for workflow"""
        return self.sites