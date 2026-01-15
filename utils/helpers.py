"""Helper functions for the Tableau UAT Configuration Tool."""

    
def generate_config_summary(site_manager=None, tenant_manager=None, project_manager=None, 
                           workbook_manager=None, datasource_manager=None, flow_manager=None):
    """Generate a summary table of the current configuration"""
    
    # Collect all resources
    all_resources = []
    
    # Add tenants from tenant manager
    for tenant in tenant_manager.resources:
        all_resources.append({
            "type": "🏢 Tenant",
            "identifier": "Tenant",
            "luid": tenant['luid'],
            "scope": tenant['scope']
        })
    
    # Add sites
    for site in site_manager.sites:
        all_resources.append({
            "type": "🌐 Site",
            "identifier": site['site_id'],
            "luid": site['site_luid'],
            "scope": site['scope']
        })
    
    # Add projects
    for project in project_manager.resources:
        all_resources.append({
            "type": "📁 Project",
            "identifier": "Project",
            "luid": project['luid'],
            "scope": project['scope']
        })
    
    # Add workbooks
    for workbook in workbook_manager.resources:
        all_resources.append({
            "type": "📊 Workbook",
            "identifier": "Workbook",
            "luid": workbook['luid'],
            "scope": workbook['scope']
        })
    
    # Add datasources
    for datasource in datasource_manager.resources:
        all_resources.append({
            "type": "🗄️ Datasource",
            "identifier": "Datasource",
            "luid": datasource['luid'],
            "scope": datasource['scope']
        })
    
    # Add flows
    for flow in flow_manager.resources:
        all_resources.append({
            "type": "🔄 Flow",
            "identifier": "Flow",
            "luid": flow['luid'],
            "scope": flow['scope']
        })
    
    if not all_resources:
        return """
        <div style='padding: 20px; background: #f8f9fa; border-radius: 8px; border: 2px dashed #dee2e6; text-align: center;'>
            <em style='color: #6c757d;'>No resources configured yet. Add resources above to see the configuration summary.</em>
        </div>
        """
    
    # Create table
    html = """
    <div style='padding: 15px; background: #f8f9fa; border-radius: 8px; border: 1px solid #dee2e6;'>
        <div style='display: flex; align-items: center; margin-bottom: 15px;'>
            <strong style='color: #0d6efd; font-size: 1.1em;'>📋 Configuration Summary</strong>
            <span style='margin-left: auto; color: #6c757d; font-size: 0.9em;'>Total: """ + str(len(all_resources)) + """ resource(s)</span>
        </div>
        <div style='overflow-x: auto;'>
            <table style='width: 100%; border-collapse: collapse; background: white; border-radius: 6px; overflow: hidden;'>
                <thead>
                    <tr style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white;'>
                        <th style='padding: 12px; text-align: left; font-weight: 600; border-bottom: 2px solid #5a67d8;'>Type</th>
                        <th style='padding: 12px; text-align: left; font-weight: 600; border-bottom: 2px solid #5a67d8;'>Identifier</th>
                        <th style='padding: 12px; text-align: left; font-weight: 600; border-bottom: 2px solid #5a67d8;'>LUID (Resource ID)</th>
                        <th style='padding: 12px; text-align: left; font-weight: 600; border-bottom: 2px solid #5a67d8;'>JWT Scope</th>
                    </tr>
                </thead>
                <tbody>
    """
    
    for idx, res in enumerate(all_resources):
        bg_color = '#ffffff' if idx % 2 == 0 else '#f8f9fa'
        html += f"""
        <tr style='background: {bg_color}; transition: background 0.2s;' 
            onmouseover="this.style.backgroundColor='#e7f1ff'" 
            onmouseout="this.style.backgroundColor='{bg_color}'">
            <td style='padding: 12px; border-bottom: 1px solid #e9ecef;'>
                <strong>{res['type']}</strong>
            </td>
            <td style='padding: 12px; border-bottom: 1px solid #e9ecef; color: #495057;'>
                {res['identifier']}
            </td>
            <td style='padding: 12px; border-bottom: 1px solid #e9ecef; font-family: monospace; font-size: 0.85em; color: #6c757d;'>
                {res['luid']}
            </td>
            <td style='padding: 12px; border-bottom: 1px solid #e9ecef;'>
                <span style='background: #e7f1ff; padding: 4px 8px; border-radius: 4px; font-size: 0.85em; color: #0d6efd;'>
                    {res['scope']}
                </span>
            </td>
        </tr>
        """
    
    html += """
                </tbody>
            </table>
        </div>
    </div>
    """
    
    return html