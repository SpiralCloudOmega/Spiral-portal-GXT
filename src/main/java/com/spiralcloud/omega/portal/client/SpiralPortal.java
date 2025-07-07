package com.spiralcloud.omega.portal.client;

import com.google.gwt.core.client.EntryPoint;
import com.google.gwt.core.client.GWT;
import com.google.gwt.dom.client.Element;
import com.google.gwt.user.client.DOM;
import com.google.gwt.user.client.ui.RootPanel;

/**
 * Entry point classes define <code>onModuleLoad()</code>.
 * 
 * SPGX - Spiral Portal GWT Application
 */
public class SpiralPortal implements EntryPoint {

    /**
     * This is the entry point method.
     */
    public void onModuleLoad() {
        // Log that the application is starting
        GWT.log("Starting Spiral Portal GWT Application...");
        
        // Hide the loading indicator
        Element loading = DOM.getElementById("loading");
        if (loading != null) {
            loading.getStyle().setProperty("display", "none");
        }
        
        // Create and setup the main portal interface
        PortalMainView mainView = new PortalMainView();
        
        // Add to the portal container or root panel
        RootPanel container = RootPanel.get("portal-container");
        if (container != null) {
            container.add(mainView);
        } else {
            RootPanel.get().add(mainView);
        }
        
        GWT.log("Spiral Portal GWT Application loaded successfully!");
    }
}