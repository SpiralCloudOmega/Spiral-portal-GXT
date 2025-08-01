package com.spiralcloud.omega.portal.client.simulation.ui;

import com.google.gwt.core.client.GWT;
import com.google.gwt.dom.client.DivElement;
import com.google.gwt.dom.client.Document;
import com.google.gwt.user.client.Timer;
import com.google.gwt.user.client.ui.*;
import com.spiralcloud.omega.portal.client.simulation.OmegaFusionRuntime;

/**
 * SimulationInterface3D - Interactive 3D visualization interface
 * 
 * Provides a WebGL/Three.js-based 3D visualization tool to render
 * stellar hypergraphs, recursive layers, and interactive glyph manipulation.
 */
public class SimulationInterface3D extends Composite {
    
    private VerticalPanel mainPanel;
    private HorizontalPanel controlPanel;
    private DivElement threejsContainer;
    private Timer animationTimer;
    private boolean isAnimating;
    
    // Control buttons
    private Button initializeVisualizationButton;
    private Button toggleAnimationButton;
    private Button resetViewButton;
    private Button generateHypergraphButton;
    
    // Info panel
    private HTML infoPanel;
    
    public SimulationInterface3D() {
        initializeComponents();
        setupLayout();
        initWidget(mainPanel);
        initializeThreeJSScene();
    }
    
    private void initializeComponents() {
        mainPanel = new VerticalPanel();
        mainPanel.setSize("100%", "100%");
        mainPanel.setSpacing(10);
        
        controlPanel = new HorizontalPanel();
        controlPanel.setSpacing(10);
        
        // Create Three.js container
        threejsContainer = Document.get().createDivElement();
        threejsContainer.setId("threejs-container");
        threejsContainer.getStyle().setProperty("width", "100%");
        threejsContainer.getStyle().setProperty("height", "500px");
        threejsContainer.getStyle().setProperty("border", "1px solid #ddd");
        threejsContainer.getStyle().setProperty("borderRadius", "8px");
        threejsContainer.getStyle().setProperty("background", "#000");
        
        // Initialize control buttons
        initializeVisualizationButton = new Button("Initialize 3D Scene");
        toggleAnimationButton = new Button("Start Animation");
        resetViewButton = new Button("Reset View");
        generateHypergraphButton = new Button("Generate Hypergraph");
        
        // Initialize info panel
        infoPanel = new HTML();
        updateInfoPanel();
        
        setupEventHandlers();
    }
    
    private void setupLayout() {
        // Add title
        HTML title = new HTML("<h2 style='color: #2c3e50; margin: 0 0 20px 0;'>Interactive 3D Simulation Interface</h2>");
        mainPanel.add(title);
        
        // Add control panel
        controlPanel.add(initializeVisualizationButton);
        controlPanel.add(toggleAnimationButton);
        controlPanel.add(resetViewButton);
        controlPanel.add(generateHypergraphButton);
        mainPanel.add(controlPanel);
        
        // Add Three.js container
        HTMLPanel containerPanel = new HTMLPanel("");
        containerPanel.getElement().appendChild(threejsContainer);
        containerPanel.setSize("100%", "500px");
        mainPanel.add(containerPanel);
        
        // Add info panel
        mainPanel.add(infoPanel);
    }
    
    private void setupEventHandlers() {
        initializeVisualizationButton.addClickHandler(event -> {
            initializeScene();
            updateInfoPanel();
        });
        
        toggleAnimationButton.addClickHandler(event -> {
            if (isAnimating) {
                stopAnimation();
                toggleAnimationButton.setText("Start Animation");
            } else {
                startAnimation();
                toggleAnimationButton.setText("Stop Animation");
            }
        });
        
        resetViewButton.addClickHandler(event -> {
            resetView();
            updateInfoPanel();
        });
        
        generateHypergraphButton.addClickHandler(event -> {
            generateNewHypergraph();
            updateInfoPanel();
        });
    }
    
    private void updateInfoPanel() {
        OmegaFusionRuntime runtime = OmegaFusionRuntime.getInstance();
        
        String content = 
            "<div style='background: #f8f9fa; padding: 15px; border-radius: 8px; margin: 10px 0; border: 1px solid #e9ecef;'>" +
            "<h4 style='margin: 0 0 10px 0; color: #2c3e50;'>3D Visualization Status</h4>" +
            "<p><strong>Runtime Mode:</strong> " + runtime.getCurrentState().getRuntimeMode() + "</p>" +
            "<p><strong>Simulation Phase:</strong> " + runtime.getCurrentState().getSimulationPhase() + "</p>" +
            "<p><strong>Animation Status:</strong> " + (isAnimating ? "Running" : "Stopped") + "</p>" +
            "<p><strong>Hypergraph Nodes:</strong> " + runtime.getCurrentState().getHypergraphNodes() + "</p>" +
            
            "<h5 style='margin: 15px 0 5px 0; color: #2c3e50;'>Visualization Features:</h5>" +
            "<ul style='margin: 5px 0; padding-left: 20px;'>" +
            "<li>Stellar hypergraph rendering with WebGL</li>" +
            "<li>Recursive reality layer visualization</li>" +
            "<li>Interactive glyph manipulation tools</li>" +
            "<li>Real-time synchronization with ΩFusionRuntime</li>" +
            "<li>3D navigation and camera controls</li>" +
            "</ul>" +
            
            "<h5 style='margin: 15px 0 5px 0; color: #2c3e50;'>Current Scene Elements:</h5>" +
            "<ul style='margin: 5px 0; padding-left: 20px;'>" +
            "<li>Hypergraph nodes and edges</li>" +
            "<li>Recursive layer representations</li>" +
            "<li>Void substrate visualization</li>" +
            "<li>Paradox resolution indicators</li>" +
            "<li>Mathematical computation displays</li>" +
            "</ul>" +
            "</div>";
        
        infoPanel.setHTML(content);
    }
    
    private void initializeThreeJSScene() {
        // Setup animation timer
        animationTimer = new Timer() {
            @Override
            public void run() {
                if (isAnimating) {
                    animateScene();
                }
            }
        };
    }
    
    private native void initializeScene() /*-{
        var container = $doc.getElementById('threejs-container');
        if (!container) return;
        
        // Clear any existing content
        container.innerHTML = '';
        
        try {
            // Create Three.js scene
            var scene = new $wnd.THREE.Scene();
            var camera = new $wnd.THREE.PerspectiveCamera(75, container.clientWidth / container.clientHeight, 0.1, 1000);
            var renderer = new $wnd.THREE.WebGLRenderer({ antialias: true });
            
            renderer.setSize(container.clientWidth, container.clientHeight);
            renderer.setClearColor(0x000011, 1);
            container.appendChild(renderer.domElement);
            
            // Create hypergraph structure
            var hypergraphGroup = new $wnd.THREE.Group();
            
            // Create nodes (spheres)
            var nodeGeometry = new $wnd.THREE.SphereGeometry(0.3, 16, 16);
            var nodeMaterial = new $wnd.THREE.MeshBasicMaterial({ color: 0x00ffff, wireframe: false });
            
            // Generate hypergraph nodes in 3D space
            var nodes = [];
            var nodeCount = 20;
            for (var i = 0; i < nodeCount; i++) {
                var node = new $wnd.THREE.Mesh(nodeGeometry, nodeMaterial);
                
                // Position nodes in a complex 3D pattern
                var phi = Math.acos(-1 + (2 * i) / nodeCount);
                var theta = Math.sqrt(nodeCount * Math.PI) * phi;
                var radius = 8;
                
                node.position.x = radius * Math.cos(theta) * Math.sin(phi);
                node.position.y = radius * Math.sin(theta) * Math.sin(phi);
                node.position.z = radius * Math.cos(phi);
                
                nodes.push(node);
                hypergraphGroup.add(node);
            }
            
            // Create edges (lines connecting nodes)
            var edgeMaterial = new $wnd.THREE.LineBasicMaterial({ color: 0x44ffaa, opacity: 0.6, transparent: true });
            
            for (var i = 0; i < nodes.length; i++) {
                for (var j = i + 1; j < nodes.length; j++) {
                    // Connect nodes with probability based on distance
                    var distance = nodes[i].position.distanceTo(nodes[j].position);
                    if (Math.random() < 0.3 && distance < 12) {
                        var geometry = new $wnd.THREE.BufferGeometry().setFromPoints([
                            nodes[i].position,
                            nodes[j].position
                        ]);
                        var line = new $wnd.THREE.Line(geometry, edgeMaterial);
                        hypergraphGroup.add(line);
                    }
                }
            }
            
            scene.add(hypergraphGroup);
            
            // Add recursive layer visualization
            var layerMaterial = new $wnd.THREE.MeshBasicMaterial({ 
                color: 0x8844ff, 
                wireframe: true, 
                opacity: 0.3, 
                transparent: true 
            });
            
            for (var layer = 0; layer < 5; layer++) {
                var layerGeometry = new $wnd.THREE.SphereGeometry(15 + layer * 3, 16, 16);
                var layerMesh = new $wnd.THREE.Mesh(layerGeometry, layerMaterial);
                scene.add(layerMesh);
            }
            
            // Position camera
            camera.position.z = 25;
            camera.position.y = 10;
            camera.lookAt(0, 0, 0);
            
            // Store references for animation
            $wnd.simulationScene = {
                scene: scene,
                camera: camera,
                renderer: renderer,
                hypergraphGroup: hypergraphGroup,
                nodes: nodes,
                animationFrame: 0
            };
            
            // Initial render
            renderer.render(scene, camera);
            
            console.log('Three.js scene initialized successfully');
            
        } catch (e) {
            console.error('Error initializing Three.js scene:', e);
            container.innerHTML = '<div style="color: white; padding: 20px; text-align: center;">' +
                                'WebGL/Three.js initialization failed.<br/>' +
                                'Please ensure your browser supports WebGL and Three.js is loaded.<br/>' +
                                'Error: ' + e.message + '</div>';
        }
    }-*/;
    
    private native void animateScene() /*-{
        if (!$wnd.simulationScene) return;
        
        try {
            var scene = $wnd.simulationScene.scene;
            var camera = $wnd.simulationScene.camera;
            var renderer = $wnd.simulationScene.renderer;
            var hypergraphGroup = $wnd.simulationScene.hypergraphGroup;
            var nodes = $wnd.simulationScene.nodes;
            
            // Increment animation frame
            $wnd.simulationScene.animationFrame += 0.01;
            var frame = $wnd.simulationScene.animationFrame;
            
            // Rotate hypergraph
            hypergraphGroup.rotation.y = frame * 0.5;
            hypergraphGroup.rotation.x = Math.sin(frame) * 0.2;
            
            // Animate individual nodes
            for (var i = 0; i < nodes.length; i++) {
                var node = nodes[i];
                var offset = i * 0.1;
                
                // Pulsing effect
                var scale = 1 + Math.sin(frame * 3 + offset) * 0.3;
                node.scale.set(scale, scale, scale);
                
                // Color cycling
                var hue = (frame + offset) % 1;
                node.material.color.setHSL(hue, 0.8, 0.6);
            }
            
            // Camera orbital movement
            var radius = 25;
            camera.position.x = Math.cos(frame * 0.2) * radius;
            camera.position.z = Math.sin(frame * 0.2) * radius;
            camera.lookAt(0, 0, 0);
            
            // Render the scene
            renderer.render(scene, camera);
            
        } catch (e) {
            console.error('Animation error:', e);
        }
    }-*/;
    
    private native void resetView() /*-{
        if (!$wnd.simulationScene) return;
        
        try {
            var camera = $wnd.simulationScene.camera;
            
            // Reset camera position
            camera.position.set(0, 10, 25);
            camera.lookAt(0, 0, 0);
            
            // Reset animation frame
            $wnd.simulationScene.animationFrame = 0;
            
            // Reset hypergraph rotation
            var hypergraphGroup = $wnd.simulationScene.hypergraphGroup;
            hypergraphGroup.rotation.set(0, 0, 0);
            
            // Render
            var renderer = $wnd.simulationScene.renderer;
            var scene = $wnd.simulationScene.scene;
            renderer.render(scene, camera);
            
            console.log('View reset');
            
        } catch (e) {
            console.error('Reset view error:', e);
        }
    }-*/;
    
    private native void generateNewHypergraph() /*-{
        if (!$wnd.simulationScene) {
            this.@com.spiralcloud.omega.portal.client.simulation.ui.SimulationInterface3D::initializeScene()();
            return;
        }
        
        try {
            var scene = $wnd.simulationScene.scene;
            var hypergraphGroup = $wnd.simulationScene.hypergraphGroup;
            
            // Clear existing hypergraph
            scene.remove(hypergraphGroup);
            
            // Create new hypergraph group
            hypergraphGroup = new $wnd.THREE.Group();
            
            // Generate new nodes with different pattern
            var nodeGeometry = new $wnd.THREE.SphereGeometry(0.3, 16, 16);
            var nodeMaterial = new $wnd.THREE.MeshBasicMaterial({ color: 0xff4400, wireframe: false });
            
            var nodes = [];
            var nodeCount = 15 + Math.floor(Math.random() * 20);
            
            for (var i = 0; i < nodeCount; i++) {
                var node = new $wnd.THREE.Mesh(nodeGeometry, nodeMaterial);
                
                // Random 3D positioning
                var radius = 5 + Math.random() * 10;
                var phi = Math.random() * Math.PI;
                var theta = Math.random() * 2 * Math.PI;
                
                node.position.x = radius * Math.sin(phi) * Math.cos(theta);
                node.position.y = radius * Math.sin(phi) * Math.sin(theta);
                node.position.z = radius * Math.cos(phi);
                
                nodes.push(node);
                hypergraphGroup.add(node);
            }
            
            // Create new edges
            var edgeMaterial = new $wnd.THREE.LineBasicMaterial({ color: 0xffaa00, opacity: 0.7, transparent: true });
            
            for (var i = 0; i < nodes.length; i++) {
                for (var j = i + 1; j < nodes.length; j++) {
                    if (Math.random() < 0.4) {
                        var geometry = new $wnd.THREE.BufferGeometry().setFromPoints([
                            nodes[i].position,
                            nodes[j].position
                        ]);
                        var line = new $wnd.THREE.Line(geometry, edgeMaterial);
                        hypergraphGroup.add(line);
                    }
                }
            }
            
            scene.add(hypergraphGroup);
            
            // Update references
            $wnd.simulationScene.hypergraphGroup = hypergraphGroup;
            $wnd.simulationScene.nodes = nodes;
            
            // Update simulation state
            var runtime = @com.spiralcloud.omega.portal.client.simulation.OmegaFusionRuntime::getInstance()();
            runtime.@com.spiralcloud.omega.portal.client.simulation.OmegaFusionRuntime::getCurrentState()()
                .@com.spiralcloud.omega.portal.client.simulation.data.SimulationState::setHypergraphNodes(I)(nodeCount);
            
            console.log('Generated new hypergraph with ' + nodeCount + ' nodes');
            
        } catch (e) {
            console.error('Generate hypergraph error:', e);
        }
    }-*/;
    
    private void startAnimation() {
        isAnimating = true;
        animationTimer.scheduleRepeating(16); // ~60 FPS
        GWT.log("3D animation started");
    }
    
    private void stopAnimation() {
        isAnimating = false;
        animationTimer.cancel();
        GWT.log("3D animation stopped");
    }
}