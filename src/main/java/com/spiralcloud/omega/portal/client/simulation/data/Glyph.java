package com.spiralcloud.omega.portal.client.simulation.data;

import java.util.ArrayList;
import java.util.List;

/**
 * Glyph - Represents a symbolic element in the simulation
 * 
 * Glyphs are fundamental symbolic structures that can be manipulated
 * within the simulation environment to affect various runtime states.
 */
public class Glyph {
    
    private String name;
    private String symbol;
    private String type;
    private double power;
    private double stability;
    private boolean isActive;
    private String effect;
    private List<String> associatedStates;
    
    public Glyph(String name, String symbol, String type) {
        this.name = name;
        this.symbol = symbol;
        this.type = type;
        this.power = 0.5 + Math.random() * 0.5; // Random power 0.5-1.0
        this.stability = 0.7 + Math.random() * 0.3; // Random stability 0.7-1.0
        this.isActive = false;
        this.effect = generateEffect();
        this.associatedStates = new ArrayList<>();
        initializeAssociatedStates();
    }
    
    private String generateEffect() {
        String[] effects = {
            "Stabilizes void fluctuations",
            "Enhances recursive depth",
            "Harmonizes paradoxes",
            "Accelerates mathematical computation",
            "Transcends ontological boundaries",
            "Amplifies existential resonance",
            "Balances reality layers",
            "Focuses hypergraph connections"
        };
        
        return effects[(int)(Math.random() * effects.length)];
    }
    
    private void initializeAssociatedStates() {
        String[] possibleStates = {
            "BEING", "NON_BEING", "POTENTIAL_BEING", "META_BEING",
            "QUANTUM_SUPERPOSITION", "PARADOXICAL_EXISTENCE", "TRANSCENDENT_STATE"
        };
        
        // Add 1-3 random associated states
        int stateCount = 1 + (int)(Math.random() * 3);
        for (int i = 0; i < stateCount; i++) {
            String state = possibleStates[(int)(Math.random() * possibleStates.length)];
            if (!associatedStates.contains(state)) {
                associatedStates.add(state);
            }
        }
    }
    
    public void activate() {
        isActive = true;
        // Activation may affect stability
        stability = Math.max(0.3, stability - 0.1 + Math.random() * 0.2);
    }
    
    public void deactivate() {
        isActive = false;
        // Deactivation may restore stability
        stability = Math.min(1.0, stability + 0.05);
    }
    
    public void processUpdate() {
        if (isActive) {
            // Active glyphs may fluctuate in power and stability
            power += (Math.random() - 0.5) * 0.1;
            power = Math.max(0.1, Math.min(1.0, power));
            
            stability += (Math.random() - 0.5) * 0.05;
            stability = Math.max(0.1, Math.min(1.0, stability));
        } else {
            // Inactive glyphs slowly stabilize
            if (stability < 0.9) {
                stability += 0.01;
            }
        }
    }
    
    public String getStatusColor() {
        if (!isActive) return "#666666";
        
        if (stability > 0.8) return "#27ae60";
        else if (stability > 0.5) return "#f39c12";
        else return "#e74c3c";
    }
    
    // Getters and setters
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    
    public String getSymbol() { return symbol; }
    public void setSymbol(String symbol) { this.symbol = symbol; }
    
    public String getType() { return type; }
    public void setType(String type) { this.type = type; }
    
    public double getPower() { return power; }
    public void setPower(double power) { this.power = power; }
    
    public double getStability() { return stability; }
    public void setStability(double stability) { this.stability = stability; }
    
    public boolean isActive() { return isActive; }
    public void setActive(boolean active) { isActive = active; }
    
    public String getEffect() { return effect; }
    public void setEffect(String effect) { this.effect = effect; }
    
    public List<String> getAssociatedStates() { return new ArrayList<>(associatedStates); }
    public void setAssociatedStates(List<String> associatedStates) { 
        this.associatedStates = new ArrayList<>(associatedStates); 
    }
}