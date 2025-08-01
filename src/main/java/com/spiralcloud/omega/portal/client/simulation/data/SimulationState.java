package com.spiralcloud.omega.portal.client.simulation.data;

/**
 * SimulationState - Maintains the overall state of the simulation
 * 
 * Contains all necessary state information for the ΩFusionRuntime
 * simulation environment.
 */
public class SimulationState {
    
    private String runtimeMode;
    private long currentTick;
    private long startTime;
    private double overallStability;
    private String simulationPhase;
    private int glyphCount;
    private int hypergraphNodes;
    private boolean ritualActive;
    
    public SimulationState() {
        this.runtimeMode = "INACTIVE";
        this.currentTick = 0;
        this.startTime = System.currentTimeMillis();
        this.overallStability = 0.0;
        this.simulationPhase = "INITIALIZATION";
        this.glyphCount = 0;
        this.hypergraphNodes = 0;
        this.ritualActive = false;
    }
    
    public void incrementTick() {
        currentTick++;
        
        // Update simulation phase based on tick count
        if (currentTick < 100) {
            simulationPhase = "INITIALIZATION";
        } else if (currentTick < 500) {
            simulationPhase = "STABILIZATION";
        } else if (currentTick < 1000) {
            simulationPhase = "EXPLORATION";
        } else if (currentTick < 2000) {
            simulationPhase = "TRANSCENDENCE";
        } else {
            simulationPhase = "OMEGA_STATE";
        }
    }
    
    public void updateOverallStability(double voidStability, double recursionStability, 
                                     double ontologyStability, double paradoxEfficiency, 
                                     double mathStability) {
        // Calculate weighted average of all stability metrics
        overallStability = (voidStability * 0.2 + 
                          recursionStability * 0.2 + 
                          ontologyStability * 0.2 + 
                          paradoxEfficiency * 0.2 + 
                          mathStability * 0.2);
    }
    
    public long getUptime() {
        return System.currentTimeMillis() - startTime;
    }
    
    public String getFormattedUptime() {
        long uptime = getUptime();
        long seconds = uptime / 1000;
        long minutes = seconds / 60;
        long hours = minutes / 60;
        
        // GWT-compatible string formatting
        String h = (hours % 24) < 10 ? "0" + (hours % 24) : "" + (hours % 24);
        String m = (minutes % 60) < 10 ? "0" + (minutes % 60) : "" + (minutes % 60);
        String s = (seconds % 60) < 10 ? "0" + (seconds % 60) : "" + (seconds % 60);
        
        return h + ":" + m + ":" + s;
    }
    
    // Getters and Setters
    public String getRuntimeMode() { return runtimeMode; }
    public void setRuntimeMode(String runtimeMode) { this.runtimeMode = runtimeMode; }
    
    public long getCurrentTick() { return currentTick; }
    public void setCurrentTick(long currentTick) { this.currentTick = currentTick; }
    
    public long getStartTime() { return startTime; }
    public void setStartTime(long startTime) { this.startTime = startTime; }
    
    public double getOverallStability() { return overallStability; }
    public void setOverallStability(double overallStability) { this.overallStability = overallStability; }
    
    public String getSimulationPhase() { return simulationPhase; }
    public void setSimulationPhase(String simulationPhase) { this.simulationPhase = simulationPhase; }
    
    public int getGlyphCount() { return glyphCount; }
    public void setGlyphCount(int glyphCount) { this.glyphCount = glyphCount; }
    
    public int getHypergraphNodes() { return hypergraphNodes; }
    public void setHypergraphNodes(int hypergraphNodes) { this.hypergraphNodes = hypergraphNodes; }
    
    public boolean isRitualActive() { return ritualActive; }
    public void setRitualActive(boolean ritualActive) { this.ritualActive = ritualActive; }
}