package com.spiralcloud.omega.portal.client.simulation.data;

import java.util.ArrayList;
import java.util.List;

/**
 * SampleDataGenerator - Provides sample data for simulation testing
 * 
 * Generates sample scroll sectors, glyphs, and hypergraph structures
 * for testing the simulation environment.
 */
public class SampleDataGenerator {
    
    public static List<Glyph> generateSampleGlyphs() {
        List<Glyph> glyphs = new ArrayList<>();
        
        // Fundamental glyphs
        glyphs.add(new Glyph("Void Anchor", "⚫", "FUNDAMENTAL"));
        glyphs.add(new Glyph("Infinity Loop", "∞", "RECURSIVE"));
        glyphs.add(new Glyph("Paradox Knot", "⚭", "PARADOXICAL"));
        glyphs.add(new Glyph("Reality Spiral", "🌀", "ONTOLOGICAL"));
        glyphs.add(new Glyph("Math Nexus", "∑", "MATHEMATICAL"));
        
        // Elemental glyphs
        glyphs.add(new Glyph("Fire Essence", "🔥", "ELEMENTAL"));
        glyphs.add(new Glyph("Water Flow", "🌊", "ELEMENTAL"));
        glyphs.add(new Glyph("Earth Core", "🗿", "ELEMENTAL"));
        glyphs.add(new Glyph("Air Vortex", "🌪", "ELEMENTAL"));
        glyphs.add(new Glyph("Void Essence", "◯", "ELEMENTAL"));
        
        // Transcendent glyphs
        glyphs.add(new Glyph("Omega Point", "Ω", "TRANSCENDENT"));
        glyphs.add(new Glyph("Alpha Source", "Α", "TRANSCENDENT"));
        glyphs.add(new Glyph("Phi Resonance", "Φ", "TRANSCENDENT"));
        glyphs.add(new Glyph("Tau Cycle", "Τ", "TRANSCENDENT"));
        glyphs.add(new Glyph("Delta Transform", "Δ", "TRANSCENDENT"));
        
        return glyphs;
    }
    
    public static List<ScrollSector> generateSampleScrollSectors() {
        List<ScrollSector> sectors = new ArrayList<>();
        
        sectors.add(new ScrollSector("Foundation Sector", 
            "Contains the basic principles of void manipulation and reality anchoring",
            new String[]{"Void Anchor", "Reality Spiral"}, 
            ScrollSector.SectorType.FOUNDATION));
            
        sectors.add(new ScrollSector("Recursion Sector",
            "Houses the infinite recursion protocols and depth management algorithms",
            new String[]{"Infinity Loop", "Math Nexus"},
            ScrollSector.SectorType.RECURSIVE));
            
        sectors.add(new ScrollSector("Paradox Sector",
            "Manages paradox resolution techniques and logical contradiction handling",
            new String[]{"Paradox Knot", "Omega Point"},
            ScrollSector.SectorType.PARADOXICAL));
            
        sectors.add(new ScrollSector("Elemental Sector",
            "Controls elemental forces and their interactions within the simulation",
            new String[]{"Fire Essence", "Water Flow", "Earth Core", "Air Vortex"},
            ScrollSector.SectorType.ELEMENTAL));
            
        sectors.add(new ScrollSector("Transcendence Sector",
            "Contains the highest-level transcendence protocols and omega-state management",
            new String[]{"Omega Point", "Alpha Source", "Phi Resonance"},
            ScrollSector.SectorType.TRANSCENDENT));
            
        return sectors;
    }
    
    public static List<HypergraphNode> generateSampleHypergraph() {
        List<HypergraphNode> nodes = new ArrayList<>();
        
        // Create fundamental nodes
        nodes.add(new HypergraphNode("Void Core", "FUNDAMENTAL", 0, 0, 0));
        nodes.add(new HypergraphNode("Reality Anchor", "FUNDAMENTAL", 5, 0, 0));
        nodes.add(new HypergraphNode("Recursion Hub", "RECURSIVE", 0, 5, 0));
        nodes.add(new HypergraphNode("Paradox Nexus", "PARADOXICAL", 0, 0, 5));
        nodes.add(new HypergraphNode("Math Engine", "MATHEMATICAL", -5, 0, 0));
        
        // Create elemental nodes
        nodes.add(new HypergraphNode("Fire Node", "ELEMENTAL", 3, 3, 0));
        nodes.add(new HypergraphNode("Water Node", "ELEMENTAL", -3, 3, 0));
        nodes.add(new HypergraphNode("Earth Node", "ELEMENTAL", 0, -3, 3));
        nodes.add(new HypergraphNode("Air Node", "ELEMENTAL", 0, 3, 3));
        
        // Create transcendent nodes
        nodes.add(new HypergraphNode("Omega Terminal", "TRANSCENDENT", 0, 0, 8));
        nodes.add(new HypergraphNode("Alpha Source", "TRANSCENDENT", 0, 0, -8));
        
        // Set up connections between nodes
        for (int i = 0; i < nodes.size(); i++) {
            HypergraphNode node = nodes.get(i);
            for (int j = i + 1; j < nodes.size(); j++) {
                HypergraphNode otherNode = nodes.get(j);
                double distance = calculateDistance(node, otherNode);
                
                // Connect nodes that are within a certain distance
                if (distance < 8 && Math.random() < 0.6) {
                    node.addConnection(otherNode.getName());
                    otherNode.addConnection(node.getName());
                }
            }
        }
        
        return nodes;
    }
    
    private static double calculateDistance(HypergraphNode a, HypergraphNode b) {
        double dx = a.getX() - b.getX();
        double dy = a.getY() - b.getY();
        double dz = a.getZ() - b.getZ();
        return Math.sqrt(dx*dx + dy*dy + dz*dz);
    }
    
    /**
     * Inner class representing a scroll sector
     */
    public static class ScrollSector {
        public enum SectorType {
            FOUNDATION, RECURSIVE, PARADOXICAL, ELEMENTAL, TRANSCENDENT
        }
        
        private String name;
        private String description;
        private String[] containedGlyphs;
        private SectorType type;
        private boolean isLoaded;
        
        public ScrollSector(String name, String description, String[] glyphs, SectorType type) {
            this.name = name;
            this.description = description;
            this.containedGlyphs = new String[glyphs.length];
            for (int i = 0; i < glyphs.length; i++) {
                this.containedGlyphs[i] = glyphs[i];
            }
            this.type = type;
            this.isLoaded = false;
        }
        
        // Getters
        public String getName() { return name; }
        public String getDescription() { return description; }
        public String[] getContainedGlyphs() { 
            String[] result = new String[containedGlyphs.length];
            for (int i = 0; i < containedGlyphs.length; i++) {
                result[i] = containedGlyphs[i];
            }
            return result;
        }
        public SectorType getType() { return type; }
        public boolean isLoaded() { return isLoaded; }
        public void setLoaded(boolean loaded) { isLoaded = loaded; }
    }
    
    /**
     * Inner class representing a hypergraph node
     */
    public static class HypergraphNode {
        private String name;
        private String type;
        private double x, y, z;
        private List<String> connections;
        private boolean isActive;
        
        public HypergraphNode(String name, String type, double x, double y, double z) {
            this.name = name;
            this.type = type;
            this.x = x;
            this.y = y;
            this.z = z;
            this.connections = new ArrayList<>();
            this.isActive = true;
        }
        
        public void addConnection(String nodeName) {
            if (!connections.contains(nodeName)) {
                connections.add(nodeName);
            }
        }
        
        // Getters
        public String getName() { return name; }
        public String getType() { return type; }
        public double getX() { return x; }
        public double getY() { return y; }
        public double getZ() { return z; }
        public List<String> getConnections() { return new ArrayList<>(connections); }
        public boolean isActive() { return isActive; }
        public void setActive(boolean active) { isActive = active; }
    }
}