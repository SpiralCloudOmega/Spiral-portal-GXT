package com.spiralcloud.omega.portal.client.simulation.monitor;

import com.google.gwt.core.client.GWT;
import com.google.gwt.user.client.Timer;
import com.google.gwt.user.client.ui.*;
import com.spiralcloud.omega.portal.client.simulation.OmegaFusionRuntime;
import com.spiralcloud.omega.portal.client.simulation.core.*;
import com.spiralcloud.omega.portal.client.simulation.data.SimulationState;

/**
 * RuntimeMonitorPanel - Real-time dashboard for simulation monitoring
 * 
 * Provides a comprehensive dashboard to track the state of all
 * ΩFusionRuntime components in real-time.
 */
public class RuntimeMonitorPanel extends Composite {
    
    private VerticalPanel mainPanel;
    private HorizontalPanel controlPanel;
    private FlowPanel metricsPanel;
    private Timer updateTimer;
    private boolean isMonitoring;
    
    // Status labels for each component
    private Label overallStatusLabel;
    private Label voidKernelStatusLabel;
    private Label recursionEngineStatusLabel;
    private Label ontologyFrameworkStatusLabel;
    private Label paradoxSystemStatusLabel;
    private Label mathEngineStatusLabel;
    
    // Metric displays
    private HTML voidMetricsDisplay;
    private HTML recursionMetricsDisplay;
    private HTML ontologyMetricsDisplay;
    private HTML paradoxMetricsDisplay;
    private HTML mathMetricsDisplay;
    
    // Control buttons
    private Button startSimulationButton;
    private Button stopSimulationButton;
    private Button resetButton;
    
    public RuntimeMonitorPanel() {
        initializeComponents();
        setupLayout();
        setupUpdateTimer();
        initWidget(mainPanel);
    }
    
    private void initializeComponents() {
        mainPanel = new VerticalPanel();
        mainPanel.setSize("100%", "100%");
        mainPanel.setSpacing(10);
        
        controlPanel = new HorizontalPanel();
        controlPanel.setSpacing(10);
        
        metricsPanel = new FlowPanel();
        
        // Initialize status labels
        overallStatusLabel = new Label("Overall Status: INACTIVE");
        voidKernelStatusLabel = new Label("Void Kernel: DORMANT");
        recursionEngineStatusLabel = new Label("Recursion Engine: DORMANT");
        ontologyFrameworkStatusLabel = new Label("Ontology Framework: DORMANT");
        paradoxSystemStatusLabel = new Label("Paradox System: DORMANT");
        mathEngineStatusLabel = new Label("Math Engine: DORMANT");
        
        // Initialize metric displays
        voidMetricsDisplay = createMetricDisplay("Void Kernel", "Initializing...");
        recursionMetricsDisplay = createMetricDisplay("Infinite Recursion Engine", "Initializing...");
        ontologyMetricsDisplay = createMetricDisplay("Meta-Ontological Framework", "Initializing...");
        paradoxMetricsDisplay = createMetricDisplay("Paradox Harmonization System", "Initializing...");
        mathMetricsDisplay = createMetricDisplay("Impossible Mathematics Engine", "Initializing...");
        
        // Initialize control buttons
        startSimulationButton = new Button("Start Simulation");
        stopSimulationButton = new Button("Stop Simulation");
        resetButton = new Button("Reset");
        
        setupEventHandlers();
    }
    
    private HTML createMetricDisplay(String title, String content) {
        HTML display = new HTML();
        display.setStyleName("metric-display");
        String html = 
            "<div style='background: white; border: 1px solid #ddd; border-radius: 8px; padding: 15px; margin: 10px; min-width: 300px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>" +
            "<h4 style='margin: 0 0 10px 0; color: #2c3e50; font-size: 16px;'>" + title + "</h4>" +
            "<div style='font-size: 14px; color: #555;'>" + content + "</div>" +
            "</div>";
        display.setHTML(html);
        return display;
    }
    
    private void setupLayout() {
        // Add title
        HTML title = new HTML("<h2 style='color: #2c3e50; margin: 0 0 20px 0;'>ΩFusionRuntime Monitor</h2>");
        mainPanel.add(title);
        
        // Add overall status
        overallStatusLabel.setStyleName("overall-status");
        mainPanel.add(overallStatusLabel);
        
        // Add control panel
        controlPanel.add(startSimulationButton);
        controlPanel.add(stopSimulationButton);
        controlPanel.add(resetButton);
        mainPanel.add(controlPanel);
        
        // Add status indicators
        VerticalPanel statusPanel = new VerticalPanel();
        statusPanel.add(voidKernelStatusLabel);
        statusPanel.add(recursionEngineStatusLabel);
        statusPanel.add(ontologyFrameworkStatusLabel);
        statusPanel.add(paradoxSystemStatusLabel);
        statusPanel.add(mathEngineStatusLabel);
        mainPanel.add(statusPanel);
        
        // Add metrics panel
        metricsPanel.add(voidMetricsDisplay);
        metricsPanel.add(recursionMetricsDisplay);
        metricsPanel.add(ontologyMetricsDisplay);
        metricsPanel.add(paradoxMetricsDisplay);
        metricsPanel.add(mathMetricsDisplay);
        
        mainPanel.add(metricsPanel);
    }
    
    private void setupEventHandlers() {
        startSimulationButton.addClickHandler(event -> {
            OmegaFusionRuntime.getInstance().enterSimulationMode();
            startMonitoring();
        });
        
        stopSimulationButton.addClickHandler(event -> {
            OmegaFusionRuntime.getInstance().exitSimulationMode();
            stopMonitoring();
        });
        
        resetButton.addClickHandler(event -> {
            OmegaFusionRuntime.getInstance().exitSimulationMode();
            stopMonitoring();
            updateDisplays();
        });
    }
    
    private void setupUpdateTimer() {
        updateTimer = new Timer() {
            @Override
            public void run() {
                if (isMonitoring) {
                    // Tick the runtime
                    OmegaFusionRuntime.getInstance().tick();
                    // Update displays
                    updateDisplays();
                }
            }
        };
    }
    
    private void startMonitoring() {
        isMonitoring = true;
        updateTimer.scheduleRepeating(250); // Update every 250ms
        GWT.log("Runtime monitoring started");
    }
    
    private void stopMonitoring() {
        isMonitoring = false;
        updateTimer.cancel();
        GWT.log("Runtime monitoring stopped");
    }
    
    private void updateDisplays() {
        OmegaFusionRuntime runtime = OmegaFusionRuntime.getInstance();
        SimulationState state = runtime.getCurrentState();
        
        // Update overall status
        overallStatusLabel.setText("Overall Status: " + state.getRuntimeMode() + 
                                 " | Phase: " + state.getSimulationPhase() + 
                                 " | Tick: " + state.getCurrentTick());
        
        // Update component status labels
        VoidKernel voidKernel = runtime.getVoidKernel();
        voidKernelStatusLabel.setText("Void Kernel: " + voidKernel.getKernelState());
        
        InfiniteRecursionEngine recursionEngine = runtime.getRecursionEngine();
        recursionEngineStatusLabel.setText("Recursion Engine: " + recursionEngine.getEngineState());
        
        MetaOntologicalFramework ontologyFramework = runtime.getOntologyFramework();
        ontologyFrameworkStatusLabel.setText("Ontology Framework: " + ontologyFramework.getFrameworkMode());
        
        ParadoxHarmonizationSystem paradoxSystem = runtime.getParadoxSystem();
        paradoxSystemStatusLabel.setText("Paradox System: " + paradoxSystem.getSystemState());
        
        ImpossibleMathematicsEngine mathEngine = runtime.getMathEngine();
        mathEngineStatusLabel.setText("Math Engine: " + mathEngine.getEngineState());
        
        // Update detailed metrics
        updateVoidMetrics(voidKernel);
        updateRecursionMetrics(recursionEngine);
        updateOntologyMetrics(ontologyFramework);
        updateParadoxMetrics(paradoxSystem);
        updateMathMetrics(mathEngine);
        
        // Update overall stability
        state.updateOverallStability(
            voidKernel.getSubstrateStability(),
            recursionEngine.getRecursionStability(),
            ontologyFramework.getExistentialStability(),
            paradoxSystem.getHarmonizationEfficiency(),
            mathEngine.getComputationalStability()
        );
    }
    
    private void updateVoidMetrics(VoidKernel voidKernel) {
        String content = 
            "<strong>State:</strong> " + voidKernel.getKernelState() + "<br/>" +
            "<strong>Void Depth:</strong> " + voidKernel.getVoidDepth() + " layers<br/>" +
            "<strong>Substrate Stability:</strong> " + formatPercentage(voidKernel.getSubstrateStability()) + "<br/>" +
            "<strong>Fluctuation Rate:</strong> " + voidKernel.getFluctuationRate() + "/tick";
        
        String html = 
            "<div style='background: white; border: 1px solid #ddd; border-radius: 8px; padding: 15px; margin: 10px; min-width: 300px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>" +
            "<h4 style='margin: 0 0 10px 0; color: #2c3e50; font-size: 16px;'>Void Kernel</h4>" +
            "<div style='font-size: 14px; color: #555;'>" + content + "</div>" +
            "</div>";
        voidMetricsDisplay.setHTML(html);
    }
    
    private void updateRecursionMetrics(InfiniteRecursionEngine recursionEngine) {
        String content = 
            "<strong>State:</strong> " + recursionEngine.getEngineState() + "<br/>" +
            "<strong>Recursion Depth:</strong> " + recursionEngine.getRecursionDepth() + " layers<br/>" +
            "<strong>Max Layers:</strong> " + recursionEngine.getMaxRecursionLayers() + "<br/>" +
            "<strong>Stability:</strong> " + formatPercentage(recursionEngine.getRecursionStability());
        
        String html = 
            "<div style='background: white; border: 1px solid #ddd; border-radius: 8px; padding: 15px; margin: 10px; min-width: 300px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>" +
            "<h4 style='margin: 0 0 10px 0; color: #2c3e50; font-size: 16px;'>Infinite Recursion Engine</h4>" +
            "<div style='font-size: 14px; color: #555;'>" + content + "</div>" +
            "</div>";
        recursionMetricsDisplay.setHTML(html);
    }
    
    private void updateOntologyMetrics(MetaOntologicalFramework ontologyFramework) {
        String content = 
            "<strong>Mode:</strong> " + ontologyFramework.getFrameworkMode() + "<br/>" +
            "<strong>Current State:</strong> " + ontologyFramework.getCurrentOntologyState() + "<br/>" +
            "<strong>Transitions:</strong> " + ontologyFramework.getStateTransitions() + "<br/>" +
            "<strong>Existential Stability:</strong> " + formatPercentage(ontologyFramework.getExistentialStability());
        
        String html = 
            "<div style='background: white; border: 1px solid #ddd; border-radius: 8px; padding: 15px; margin: 10px; min-width: 300px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>" +
            "<h4 style='margin: 0 0 10px 0; color: #2c3e50; font-size: 16px;'>Meta-Ontological Framework</h4>" +
            "<div style='font-size: 14px; color: #555;'>" + content + "</div>" +
            "</div>";
        ontologyMetricsDisplay.setHTML(html);
    }
    
    private void updateParadoxMetrics(ParadoxHarmonizationSystem paradoxSystem) {
        String content = 
            "<strong>State:</strong> " + paradoxSystem.getSystemState() + "<br/>" +
            "<strong>Active Paradoxes:</strong> " + paradoxSystem.getParadoxCount() + "<br/>" +
            "<strong>Resolved:</strong> " + paradoxSystem.getResolvedParadoxes() + "<br/>" +
            "<strong>Efficiency:</strong> " + formatPercentage(paradoxSystem.getHarmonizationEfficiency());
        
        String html = 
            "<div style='background: white; border: 1px solid #ddd; border-radius: 8px; padding: 15px; margin: 10px; min-width: 300px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>" +
            "<h4 style='margin: 0 0 10px 0; color: #2c3e50; font-size: 16px;'>Paradox Harmonization System</h4>" +
            "<div style='font-size: 14px; color: #555;'>" + content + "</div>" +
            "</div>";
        paradoxMetricsDisplay.setHTML(html);
    }
    
    private void updateMathMetrics(ImpossibleMathematicsEngine mathEngine) {
        String content = 
            "<strong>State:</strong> " + mathEngine.getEngineState() + "<br/>" +
            "<strong>Active Calculations:</strong> " + mathEngine.getActiveCalculationCount() + "<br/>" +
            "<strong>Completed:</strong> " + mathEngine.getCompletedCalculations() + "<br/>" +
            "<strong>Stability:</strong> " + formatPercentage(mathEngine.getComputationalStability());
        
        String html = 
            "<div style='background: white; border: 1px solid #ddd; border-radius: 8px; padding: 15px; margin: 10px; min-width: 300px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>" +
            "<h4 style='margin: 0 0 10px 0; color: #2c3e50; font-size: 16px;'>Impossible Mathematics Engine</h4>" +
            "<div style='font-size: 14px; color: #555;'>" + content + "</div>" +
            "</div>";
        mathMetricsDisplay.setHTML(html);
    }
    
    private String formatPercentage(double value) {
        // GWT-compatible percentage formatting
        int percentage = (int)(value * 1000); // Get 3 decimal places
        double displayValue = percentage / 10.0; // Convert back to 1 decimal place
        return displayValue + "%";
    }
}