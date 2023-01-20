import React, {Component} from 'react';
import {Network} from "vis-network";
import {DataSet} from "vis-data";
import PropTypes from "prop-types";

const isEqual = (...objects) => objects.every(obj => JSON.stringify(obj) === JSON.stringify(objects[0]));

export const ClusteringOptions = PropTypes.shape({
    joinCondition: PropTypes.string,
    processProperties: PropTypes.string,
    clusterNodeProperties: PropTypes.object,
    clusterEdgeProperties: PropTypes.object,
});
export const FocusOptions = PropTypes.shape({
    scale: PropTypes.number,
    offset: PropTypes.shape({
        x: PropTypes.number,
        y: PropTypes.number
    }),
    locked: PropTypes.bool,
    animation: PropTypes.oneOfType([
        PropTypes.bool,
        PropTypes.shape({
            duration: PropTypes.number,
            easingFunction: PropTypes.string
        })
    ])
});
export const MoveToOptions = PropTypes.shape({
    position: PropTypes.shape({
        x: PropTypes.number,
        y: PropTypes.number
    }),
    scale: PropTypes.number,
    offset: PropTypes.shape({
        x: PropTypes.number,
        y: PropTypes.number
    }),
    animation: PropTypes.oneOfType([
        PropTypes.bool,
        PropTypes.shape({
            duration: PropTypes.number,
            easingFunction: PropTypes.string
        })
    ])
});
export const FitOptions = PropTypes.shape({
    nodes: PropTypes.oneOfType([
        PropTypes.arrayOf(PropTypes.string),
        PropTypes.arrayOf(PropTypes.number)
    ]),
    minZoomLevel: PropTypes.number,
    maxZoomLevel: PropTypes.number,
    animation: PropTypes.oneOfType([
        PropTypes.bool,
        PropTypes.shape({
            duration: PropTypes.number,
            easingFunction: PropTypes.string
        })
    ])
});

function withoutProperties(obj, props) {
    const { [props]: unused, ...rest } = obj;
    return rest
}

/**
 * A full implementation of [vis.js](https://visjs.github.io/vis-network/docs/network/)
 * Network component for Dash Plotly.
 * Useful for displaying dynamic, automatically organised, customizable network views.
 */
export default class DashNetwork extends Component {

    constructor(props) {
        super(props);
        this.nodes = new DataSet()
        this.edges = new DataSet()
        this.net = 0
        this.active_functions = {}
        this.state = {canvasToDOM: null, DOMtoCanvas: null}
    }

    prepareOptions(options) {

        try {
            if (typeof(options.manipulation.addNode) === 'string') {
                options.manipulation.addNode = this.convertStringToFunction(options.manipulation.addNode);
            } else {
                delete options.manipulation.addNode;
            }
        } catch (exception) {
            console.log("Error: failed to parse input addNode function string");
        }

        try {
            if (typeof(options.manipulation.addEdge) === 'string') {
                options.manipulation.addEdge = this.convertStringToFunction(options.manipulation.addEdge);
            } else {
                delete options.manipulation.addEdge;
            }
        } catch (exception) {
            console.log("Error: failed to parse input addEdge function string");
        }

        try {
            if (typeof(options.manipulation.editNode) === 'string') {
                options.manipulation.editNode = this.convertStringToFunction(options.manipulation.editNode);
            } else {
                delete options.manipulation.editNode;
            }
        } catch (exception) {
            console.log("Error: failed to parse input editNode function string");
        }

        try {
            if (typeof(options.manipulation.editEdge) === 'string') {
                options.manipulation.editEdge = this.convertStringToFunction(options.manipulation.editEdge);
            } else {
                delete options.manipulation.editEdge;
            }
        } catch (exception) {
            console.log("Error: failed to parse input editEdge function string");
        }

        try {
            if (typeof(options.manipulation.deleteNode) === 'string') {
                options.manipulation.deleteNode = this.convertStringToFunction(options.manipulation.deleteNode);
            } else {
                delete options.manipulation.deleteNode;
            }
        } catch (exception) {
            console.log("Error: failed to parse input deleteNode function string");
        }

        try {
            if (typeof(options.manipulation.deleteEdge) === 'string') {
                options.manipulation.deleteEdge = this.convertStringToFunction(options.manipulation.deleteEdge);
            } else {
                delete options.manipulation.deleteEdge;
            }
        } catch (exception) {
            console.log("Error: failed to parse input deleteEdge function string");
        }
        
        try {
            if (typeof(options.nodes.ctxRenderer) === 'string') {
                options.nodes.ctxRenderer = this.convertStringToFunction(options.nodes.ctxRenderer);
            } else {
                delete options.nodes.ctxRenderer;
            }
        } catch (exception) {
            console.log("Error: failed to parse input ctxRenderer function string");
        }

        try {
            for (const [key, value] of Object.entries(options.groups)) {
                if (typeof(value.shape) === 'string' && value.shape.startsWith('custom')) {
                    if (typeof(value.ctxRenderer) === 'string') {
                        value.ctxRenderer = this.convertStringToFunction(value.ctxRenderer);

                    }
                }
            }

        } catch (exception) {
            console.log("Error: failed to parse input group function string");
        }

        return options;
    }

    componentDidMount() {
        const {id, data, options, enableHciEvents, enablePhysicsEvents, enableOtherEvents, setProps} = this.props;

        const hci_events = [
            'click','doubleClick','oncontext','hold','release','select','selectNode','selectEdge','deselectNode',
            'deselectEdge','dragStart','dragging','dragEnd','controlNodeDragging','controlNodeDragEnd','hoverNode',
            'blurNode','hoverEdge','blurEdge','zoom','showPopup','hidePopup',
        ]

        const physics_events = [
            'startStabilizing','stabilizationProgress','stabilizationIterationsDone','stabilized',
        ]

        const other_events = [
            'resize', 'initRedraw', 'beforeDrawing', 'afterDrawing', 'animationFinished', 'configChange',
        ]

        const gd = document.getElementById(id);
        this.nodes.add(data.nodes)
        this.edges.add(data.edges)

        this.net = new Network(gd, {nodes: this.nodes, edges: this.edges}, this.prepareOptions(options))
        this.registerGroupCallbacks(enableHciEvents, hci_events, this.props, setProps);
        this.registerGroupCallbacks(enablePhysicsEvents, physics_events, this.props, setProps);
        this.registerGroupCallbacks(enableOtherEvents, other_events, this.props, setProps);

        // Set some static props from the network
        setProps( { getSeed: this.net.getSeed() } );
    }

    registerGroupCallbacks(enableHciEvents, all_events, props, setProps) {
        let group_events = enableHciEvents;
        if (enableHciEvents === true) {
            group_events = all_events
        } else if (enableHciEvents === false) {
            group_events = []
        }
        // Ensure that only valid event names are being listened to; ignore everything else
        if(group_events && group_events.length > 0){
            group_events = group_events.filter(e => all_events.includes(e))
        }
        // Register Grouped Events Callbacks
        this.registerCallbacks(group_events, props, setProps);
    }

    registerCallbacks(group_events, props, setProps) {
        for (let i = 0; i < group_events.length; i++) {
            let event_name = group_events[i];
            this.net.on(event_name, function (params) {
                // deselectNode and deselectEdge have circular references which need to be removed first before serialization can proceed
                if (event_name === 'deselectNode' || event_name === 'deselectEdge') {

                   params['previousSelection']['edges'] = params['previousSelection']['edges'].map(edge => {
                       return {
                            id: edge.id,
                       };
                   });

                   params['previousSelection']['nodes'] = params['previousSelection']['nodes'].map(node => {
                       return {
                            id: node.id,
                       };
                   });
                }

                if (setProps) {
                    let cur_event = event_name;
                    if (props[cur_event] !== params) {
                        params[cur_event + " ID"] = Math.floor(Math.random() * 100);
                    }
                    setProps({[cur_event]: params});
                }
            });
        }
    }

    convertStringToFunction(function_string) {
        try {
            return new Function('return ' + function_string)();
        } catch (exception) {
            console.log("Error: failed to parse input function string");
            return null;
        }
    }

    createClusterOptions(cluster_options) {
        try {
            let cluster_options_obj = {};
            if (cluster_options) {
                cluster_options_obj = {
                    joinCondition: this.convertStringToFunction(cluster_options.joinCondition),
                    processProperties: this.convertStringToFunction(cluster_options.processProperties),
                    clusterNodeProperties: cluster_options.clusterNodeProperties,
                    clusterEdgeProperties: cluster_options.clusterEdgeProperties,
                }
            }
            return cluster_options_obj;
        } catch (exception) {
            console.log("Error: failed to parse input cluster options");
            return null;
        }
    }


    componentDidUpdate(nextProps) {

        const {setProps} = this.props;

        if (this.props.data !== nextProps.data) {
            const new_id_nodes = this.props.data.nodes.map(function (x) {
                return x.id
            })
            const remove_aim_nodes = this.nodes.getIds().filter(function (x) {
                return new_id_nodes.indexOf(x) === -1
            })
            this.nodes.remove(remove_aim_nodes)
            this.nodes.update(this.props.data.nodes)

            const new_id_edges = this.props.data.edges.map(function (x) {
                return x.id
            })
            const remove_aim_edges = this.edges.getIds().filter(function (x) {
                return new_id_edges.indexOf(x) === -1
            })
            this.edges.remove(remove_aim_edges)
            this.edges.update(this.props.data.edges)

            setProps({ data: this.props.data })
        }

        if (this.props.options !== nextProps.options) {
            this.net.setOptions(this.prepareOptions(nextProps.options));
        }

        // Handle destroy action
        if (nextProps.destroy === true){
            this.net.destroy()
        }

        // Handle on, off, once 'function' calls
        if (nextProps.on && this.props.on !== nextProps.on) {
            let func = this.convertStringToFunction(nextProps.on.callback)
            if (func) {
                this.net.on(nextProps.on.event_name, func);
                this.active_functions[func.name] = func
                setProps(this.props.on, nextProps.on);
            }
        }

        if (nextProps.off && this.props.off !== nextProps.off) {
            let func = null;
            let func_pointer = null;
            if (nextProps.off.callback) {
                func = this.convertStringToFunction(nextProps.off.callback)
                func_pointer = this.active_functions[func.name];
            }

            if (func) {
                this.net.off(nextProps.off.event_name, func_pointer);
                delete this.active_functions[func.name]
                setProps(this.props.off, nextProps.off);
            }
        }

        if (nextProps.once && this.props.once !== nextProps.once) {
            let func = this.convertStringToFunction(nextProps.once.callback)
            if (func) {
                this.net.once(nextProps.once.event_name, func);
                setProps(this.props.once, nextProps.once);
            }
        }

        // Handle canvasToDOM function call
        if ( isEqual(this.state.canvasToDOM, this.props.canvasToDOM) === false ) {
            const conversion_results = this.net.canvasToDOM(this.props.canvasToDOM);
            const conversion_obj = {x: conversion_results.x, y: conversion_results.y};
            setProps( { canvasToDOM: conversion_obj } );
            this.state.canvasToDOM = conversion_obj;
        }

        // Handle DOMtoCanvas function call
        if ( isEqual(this.state.DOMtoCanvas, this.props.DOMtoCanvas) === false ) {
            const conversion_results = this.net.DOMtoCanvas(this.props.DOMtoCanvas);
            const conversion_obj = {x: conversion_results.x, y: conversion_results.y};
            setProps( { DOMtoCanvas: conversion_obj } );
            this.state.DOMtoCanvas = conversion_obj;
        }

        // Handle redraw action
        if (nextProps.redraw === true){
            this.net.redraw();
        }

        // Handle setSize action
        if (nextProps.setSize !== this.props.setSize){
            this.net.setSize(nextProps.setSize.width, nextProps.setSize.height);
            setProps(this.props.setSize, nextProps.setSize);
        }

        // Handle cluster action
        if (nextProps.cluster !== this.props.cluster){
            const cluster_options = this.createClusterOptions(this.props.cluster.options);
            try {
                this.net.cluster(cluster_options);
                setProps( { cluster: this.props.cluster } );
            } catch (exception) {
                console.log("Error: failed to cluster");
            }
        }

        // Handle cluster by connection action
        if (nextProps.clusterByConnection !== this.props.clusterByConnection){
            const cluster_options = this.createClusterOptions(this.props.clusterByConnection.options);
            try {
                this.net.clusterByConnection(this.props.clusterByConnection.nodeId, cluster_options);
                setProps( { clusterByConnection: this.props.clusterByConnection } );
            } catch (exception) {
                console.log("Error: failed to cluster by connection");
            }
        }

        // Handle cluster by hubsize action
        if (nextProps.clusterByHubsize !== this.props.clusterByHubsize){
            const cluster_options = this.createClusterOptions(this.props.clusterByHubsize.options);
            try {
                this.net.clusterByHubsize(this.props.clusterByHubsize.hubsize, cluster_options);
                setProps( { clusterByHubsize: this.props.clusterByHubsize } );
            } catch (exception) {
                console.log("Error: failed to cluster by hubsize");
            }
        }

        // Handle cluster outliers
        if (nextProps.clusterOutliers !== this.props.clusterOutliers){
            const cluster_options = this.createClusterOptions(this.props.clusterOutliers.options);
            try {
                this.net.clusterOutliers(cluster_options);
                setProps( { clusterOutliers: this.props.clusterOutliers } );
            } catch (exception) {
                console.log("Error: failed to cluster outliers");
            }
        }

        // Handle find node
        if (nextProps.findNode !== this.props.findNode){
            try {
                const search_results = this.net.findNode(this.props.findNode.nodeId);
                setProps( { findNode: { nodeId: this.props.findNode.nodeId, result: search_results.map(String) } } );
            } catch (exception) {
                console.log("Error: failed to find node");
            }
        }

        // Handle getClusteredEdges
        if (nextProps.getClusteredEdges !== this.props.getClusteredEdges){
            try {
                const search_results = this.net.getClusteredEdges(this.props.getClusteredEdges.baseEdgeId);
                setProps( { getClusteredEdges: { baseEdgeId: this.props.getClusteredEdges.baseEdgeId,
                        result: search_results.map(String) } } );
            } catch (exception) {
                console.log("Error: failed to get clustered edges");
            }
        }

        // Handle getBaseEdges
        if (nextProps.getBaseEdges !== this.props.getBaseEdges){
            try {
                const search_results = this.net.getBaseEdges(this.props.getBaseEdges.clusteredEdgeId);
                setProps( { getBaseEdges: { clusteredEdgeId: this.props.getBaseEdges.clusteredEdgeId,
                        result: search_results.map(String) } } );
            } catch (exception) {
                console.log("Error: failed to get base edges");
            }
        }

        // Handle update edge
        if (nextProps.updateEdge !== this.props.updateEdge){
            try {
                this.net.updateEdge(this.props.updateEdge.startEdgeId, this.props.updateEdge.options);
                setProps( { updateEdge: this.props.updateEdge } );
            } catch (exception) {
                console.log("Error: failed to update edge");
            }
        }

        // Handle update clustered node
        if (nextProps.updateClusteredNode !== this.props.updateClusteredNode){
            try {
                this.net.updateClusteredNode(this.props.updateClusteredNode.clusteredNodeId,
                    this.props.updateClusteredNode.options);
                setProps( { updateClusteredNode: this.props.updateClusteredNode } );
            } catch (exception) {
                console.log("Error: failed to update node");
            }
        }

        // Handle is cluster
        if (nextProps.isCluster !== this.props.isCluster){
            try {
                const result = this.net.isCluster(this.props.isCluster.nodeId);
                setProps( { isCluster: { nodeId: this.props.isCluster.nodeId, result: result } } );
            } catch (exception) {
                console.log("Error: failed check if is cluster");
            }
        }

        // Handle get nodes in cluster
        if (nextProps.getNodesInCluster !== this.props.getNodesInCluster){
            try {
                const search_results = this.net.getNodesInCluster(this.props.getNodesInCluster.clusteredNodeId);
                setProps( { getNodesInCluster: { clusteredNodeId: this.props.getNodesInCluster.clusteredNodeId,
                        result: search_results.map(String) } } );
            } catch (exception) {
                console.log("Error: failed to get nodes in cluster");
            }
        }

        // Handle open cluster
        if (nextProps.openCluster !== this.props.openCluster){
            try {
                this.net.openCluster(this.props.openCluster.nodeId, this.props.openCluster.options);
                setProps( { openCluster: this.props.openCluster } );
            } catch (exception) {
                console.log("Error: failed to open cluster");
            }
        }

        // Handle manipulation methods
        if (nextProps.enableEditMode === true){
            this.net.enableEditMode()
        }

        if (nextProps.disableEditMode === true){
            this.net.disableEditMode()
        }

        if (nextProps.addNodeMode === true){
            this.net.addNodeMode()
        }

        if (nextProps.editNode === true){
            this.net.editNode()
        }

        if (nextProps.addEdgeMode === true){
            this.net.addEdgeMode()
        }

        if (nextProps.editEdgeMode === true){
            this.net.editEdgeMode()
        }

        if (nextProps.deleteSelected === true){
            this.net.deleteSelected()
        }

        // Handle methods to get information on nodes and edges
        // Handle getPositions function calls
        if (nextProps.getPositions !== this.props.getPositions){
            if(this.props.getPositions !== null) {
                try {
                    const positions = this.net.getPositions(this.props.getPositions.nodeIds);
                    setProps({
                        getPositions: {
                            nodeIds: this.props.getPositions.nodeIds,
                            result: positions
                        }
                    });
                } catch (exception) {
                    console.log("Error: failed to get positions");
                }
            }
        }

        // Handle getPosition function call
        if (nextProps.getPosition !== this.props.getPosition){
            if(this.props.getPosition !== null) {
                try {
                    const position = this.net.getPosition(this.props.getPosition.nodeId);
                    setProps( { getPosition: { nodeId: this.props.getPosition.nodeId,
                            result: position } } );
                } catch (exception) {
                    console.log("Error: failed to get node position");
                }
            }
        }

        // Handle storePositions function call
        if (nextProps.storePositions === true){
            this.net.storePositions()
        }

        // Handle moveNode function call
        if (nextProps.moveNode !== this.props.moveNode){
            if(this.props.moveNode !== null) {
                try {
                    this.net.moveNode(this.props.moveNode.nodeId,
                        this.props.moveNode.x, this.props.moveNode.y);
                    setProps({
                        moveNode: {
                            nodeId: this.props.moveNode.nodeId,
                            x: this.props.moveNode.x, y: this.props.moveNode.y
                        }
                    });
                } catch (exception) {
                    console.log("Error: failed to move node");
                }
            }
        }

        // Handle getBoundingBox function call
        if (nextProps.getBoundingBox !== this.props.getBoundingBox){
            try {
                const boundingBox = this.net.getBoundingBox(this.props.getBoundingBox.nodeId);
                setProps({
                    getBoundingBox: {
                        nodeId: this.props.getBoundingBox.nodeId,
                        result: boundingBox
                    }
                });
            } catch (exception) {
                console.log("Error: failed to get the bounding box");
            }
        }

        // Handle getConnectedNodes function call
        if (nextProps.getConnectedNodes !== this.props.getConnectedNodes){
            if(this.props.getConnectedNodes !== null) {
                try {
                    const connectedNodes = this.net.getConnectedNodes(this.props.getConnectedNodes.nodeId,
                        this.props.getConnectedNodes.direction);
                    setProps({
                        getConnectedNodes: {
                            nodeId: this.props.getConnectedNodes.nodeId,
                            direction: this.props.getConnectedNodes.direction,
                            result: connectedNodes
                        }
                    });
                } catch (exception) {
                    console.log("Error: failed to get the connected nodes");
                }
            }
        }

        // Handle getConnectedEdges function call
        if (nextProps.getConnectedEdges !== this.props.getConnectedEdges){
            if(this.props.getConnectedEdges !== null) {
                try {
                    const connectedEdges = this.net.getConnectedEdges(this.props.getConnectedEdges.nodeId);
                    setProps({
                        getConnectedEdges: {
                            nodeId: this.props.getConnectedEdges.nodeId,
                            result: connectedEdges
                        }
                    });
                } catch (exception) {
                    console.log("Error: failed to get the connected edges");
                }
            }
        }

        // Handle physics events
        if (nextProps.startSimulation === true){
            this.net.startSimulation()
        }

        if (nextProps.stopSimulation === true){
            this.net.stopSimulation()
        }

        // Handle stabilize function call
        if (nextProps.stabilize !== this.props.stabilize){
            if (this.props.stabilize !== null) {
                try {
                    this.net.stabilize(this.props.stabilize);
                    setProps({stabilize: this.props.stabilize});
                } catch (exception) {
                    console.log("Error: failed to stabilize network");
                }
            }
        }

        // Update getSelection
        if (this.net.getSelection() !== this.props.getSelection) {
            setProps({getSelection: this.net.getSelection()});
        }

        // Update getSelectedNodes
        if (this.net.getSelectedNodes() !== this.props.getSelectedNodes) {
            setProps({getSelectedNodes: this.net.getSelectedNodes()});
        }

        // Update getSelectedEdges
        if (this.net.getSelectedEdges() !== this.props.getSelectedEdges) {
            setProps({getSelectedEdges: this.net.getSelectedEdges()});
        }

        // Handle getNodeAt function call
        if (nextProps.getNodeAt !== this.props.getNodeAt){
            try {
                const node_at = this.net.getNodeAt(this.props.getNodeAt.position.x,
                    this.props.getNodeAt.position.y);
                setProps( { getNodeAt: { id: this.props.getNodeAt.position,
                        result: node_at } } );
            } catch (exception) {
                console.log("Error: failed to get node at");
            }
        }

        // Handle getEdgeAt function call
        if (nextProps.getEdgeAt !== this.props.getEdgeAt){
            try {
                const edge_at = this.net.getEdgeAt(this.props.getEdgeAt.position.x,
                    this.props.getEdgeAt.position.y);
                setProps( { getEdgeAt: { id: this.props.getEdgeAt.position,
                        result: edge_at } } );
            } catch (exception) {
                console.log("Error: failed to get edge at");
            }
        }

        // Handle selectNodes function call
        if (nextProps.selectNodes !== this.props.selectNodes){
            if(this.props.selectNodes !== null) {
                try {
                    this.net.selectNodes(this.props.selectNodes.nodeIds,
                        this.props.selectNodes.highlightEdges);
                    setProps({selectNodes: this.props.selectNodes});
                } catch (exception) {
                    console.log("Error: failed to select nodes");
                }
            }
        }

        // Handle selectEdges function call
        if (nextProps.selectEdges !== this.props.selectEdges){
            if (this.props.selectEdges !== null) {
                try {
                    this.net.selectEdges(this.props.selectEdges.nodeIds);
                    setProps({selectEdges: this.props.selectEdges});
                } catch (exception) {
                    console.log("Error: failed to select edges");
                }
            }
        }

        // Handle setSelection function call
        if (nextProps.setSelection !== this.props.setSelection){
            if (this.props.setSelection !== null) {
                try {
                    this.net.setSelection(this.props.setSelection.selection,
                        this.props.setSelection.options);
                    setProps({setSelection: this.props.setSelection});

                } catch (exception) {
                    console.log("Error: failed to set selection");
                }
            }
        }

        // Handle unselectAll function call
        if (nextProps.unselectAll === true){
            this.net.unselectAll()
        }

        // Update getScale
        if (this.net.getScale() !== this.props.getScale) {
            setProps({getScale: this.net.getScale()});
        }

        // Update getViewPosition
        if (this.net.getViewPosition() !== this.props.getViewPosition) {
            setProps({getViewPosition: this.net.getViewPosition()});
        }

        // Handle focus function call
        if (nextProps.focus !== this.props.focus){
            try {
                this.net.focus(this.props.focus.nodeId,
                    this.props.focus.options);
                setProps( { focus: this.props.focus } );
            } catch (exception) {
                console.log("Error: failed to focus on node");
                console.log(exception);
            }
        }

        // Handle moveTo function call
        if (nextProps.moveTo !== this.props.moveTo){
            try {
                this.net.moveTo(this.props.moveTo.options);
                setProps( { moveTo: this.props.moveTo } );
            } catch (exception) {
                console.log("Error: failed to move to on network");
            }
        }

        // Handle fit function call
        if (nextProps.fit !== this.props.fit){
            try {
                this.net.fit(this.props.fit.options);
                setProps( { fit: this.props.fit } );
            } catch (exception) {
                console.log("Error: failed to fit the network");
                console.log(exception);
            }
        }

        // Handle releaseNode function call
        if (nextProps.releaseNode === true){
            this.net.releaseNode()
        }

        // Update getOptionsFromConfigurator
        if (this.net.getOptionsFromConfigurator() !== this.props.getOptionsFromConfigurator) {
            setProps({getOptionsFromConfigurator: this.net.getOptionsFromConfigurator()});
        }

    }

    render() {
        const {id, style} = this.props;

        return (
            <div id={id} style={style}></div>
        );
    }

}

DashNetwork.propTypes = {
    /**
     * The ID used to identify this component in Dash callbacks.
     */
    id: PropTypes.string.isRequired,

    /**
     * Graph data object describing the graph to be drawn.
     * Pass a dict with two keys - 'nodes' and 'edges', set according to the vis.js documentation.
     * In Dash, this property also replaces vis.js setData function.
     * See https://visjs.github.io/vis-network/docs/network/#data
     */
    data: PropTypes.exact({
        nodes: PropTypes.arrayOf(PropTypes.object),
        edges: PropTypes.arrayOf(PropTypes.object)
    }),

    /**
     * A graph configuration object.
     * Pass a dict set according to your preferences / usecase as per the vis.js documentation.
     * In Dash, this property also replaces vis.js setOptions function.
     * See https://visjs.github.io/vis-network/docs/network/#options
     */
    options: PropTypes.object,

    /**
     * Defines CSS styles which will override styles previously set.
     */
    style: PropTypes.object,

    /**
     * Either a boolean indicating if all event callbacks, triggered by human interaction, selection, dragging etc.,
     * should be enabled, or a list of strings
     * indicating which ones should be used. If it's a list, you will need to specify one of the
     * following events: `click`, `doubleClick`, `oncontext`, `hold`, 'release', 'select',
     * 'selectNode', 'selectEdge', 'deselectNode', 'deselectEdge', 'dragStart', 'dragging', 'dragEnd',
     * 'controlNodeDragging', 'controlNodeDragEnd', 'hoverNode', 'blurNode', 'hoverEdge', 'blurEdge',
     * 'zoom', 'showPopup', 'hidePopup'.
     * See https://visjs.github.io/vis-network/docs/network/#events for more details
     */
    enableHciEvents: PropTypes.oneOfType([
        PropTypes.arrayOf(PropTypes.string), PropTypes.bool
    ]),

    /**
     * Read-only prop. To use this, make sure that `enableHciEvents` is set to `True`, or that `enableHciEvents` is a list that contains this event type.
     * Fired when the user clicks the mouse of taps on a touchscreen device.
     * {
     *   nodes: [Array of selected nodeIds],
     *   edges: [Array of selected edgeIds],
     *   event: [Object] original click event,
     *   pointer: {
     *     DOM: {x:pointer_x, y:pointer_y},
     *     canvas: {x:canvas_x, y:canvas_y}
     *   }
     * }
     *
     * This is the structure common to all events. Specifically for the click event, the following property is added:
     *
     * {
     * ...
     *   items: [Array of click items],
     * }
     *
     * Where the click items can be:
     *   {nodeId:NodeId}            // node with given id clicked on
     *   {nodeId:NodeId labelId:0}  // label of node with given id clicked on
     *   {edgeId:EdgeId}            // edge with given id clicked on
     *   {edge:EdgeId, labelId:0}   // label of edge with given id clicked onThe order of the items array is descending in z-order. Thus, to get the topmost item, get the value at index 0.
     */
    click: PropTypes.object,

    /**
     * Read-only prop. To use this, make sure that `enableHciEvents` is set to `True`, or that `enableHciEvents` is a list that contains this event type.
     * Fired when the user double clicks the mouse or double taps on a touchscreen device.
     * Since a double click is in fact 2 clicks, 2 click events are fired, followed by a double click event.
     * If you do not want to use the click events if a double click event is fired, just check the time
     * between click events before processing them.
     */
    doubleClick: PropTypes.object,

    /**
     * Read-only prop. To use this, make sure that `enableHciEvents` is set to `True`, or that `enableHciEvents` is a list that contains this event type.
     *    Fired when the user click on the canvas with the right mouse button.
     *    The right mouse button does not select by default.
     *    You can use the method getNodeAt to select the node if you want.
     */
    oncontext: PropTypes.object,

    /**
     * Read-only prop. To use this, make sure that `enableHciEvents` is set to `True`, or that `enableHciEvents` is a list that contains this event type.
     *    Fired when the user clicks and holds the mouse or taps and holds on a touchscreen device.
     *    A click event is also fired in this case.
     */
    hold: PropTypes.object,

    /**
     * Read-only prop. To use this, make sure that `enableHciEvents` is set to `True`, or that `enableHciEvents` is a list that contains this event type.
     * Fired after drawing on the canvas has been completed. Can be used to draw on top of the network.
     */
    release: PropTypes.object,

    /**
     * Read-only prop. To use this, make sure that `enableHciEvents` is set to `True`, or that `enableHciEvents` is a list that contains this event type.
     * Contains a list of selected nodes and edges.
     * Struct is updated when a click, double click, context click, hold and release is performed on the graph.
     */
    select: PropTypes.object,

    /**
     * Read-only prop. To use this, make sure that `enableHciEvents` is set to `True`, or that `enableHciEvents` is a list that contains this event type.
     * Fired when a node has been selected by the user.
     */
    selectNode: PropTypes.object,

    /**
     * Read-only prop. To use this, make sure that `enableHciEvents` is set to `True`, or that `enableHciEvents` is a list that contains this event type.
     * Fired when an edge has been selected by the user.
     */
    selectEdge: PropTypes.object,

    /**
     * Read-only prop. To use this, make sure that `enableHciEvents` is set to `True`, or that `enableHciEvents` is a list that contains this event type.
     * Fired when a node (or nodes) has (or have) been deselected by the user.
     * The previous selection is the list of nodes and edges that were selected before the last user event.
     * Passes an object with properties structured as:
     * {
     *   nodes: [Array of selected nodeIds],
     *   edges: [Array of selected edgeIds],
     *   event: [Object] original click event,
     *   pointer: {
     *     DOM: {x:pointer_x, y:pointer_y},
     *     canvas: {x:canvas_x, y:canvas_y}
     *     }
     *   },
     *   previousSelection: {
     *     nodes: [Array of previously selected nodeIds],
     *     edges: [Array of previously selected edgeIds]
     *   }
     * }
     */
    deselectNode: PropTypes.object,

    /**
     * Read-only prop. To use this, make sure that `enableHciEvents` is set to `True`, or that `enableHciEvents` is a list that contains this event type.
     * Fired when an edge (or edges) has (or have) been deselected by the user.
     * The previous selection is the list of nodes and edges that were selected before the last user event.
     */
    deselectEdge: PropTypes.object,

    /**
     * Read-only prop. To use this, make sure that `enableHciEvents` is set to `True`, or that `enableHciEvents` is a list that contains this event type.
     * Fired when starting a drag.
     */
    dragStart: PropTypes.object,

    /**
     * Read-only prop. To use this, make sure that `enableHciEvents` is set to `True`, or that `enableHciEvents` is a list that contains this event type.
     * Fired when dragging node(s) or the view.
     */
    dragging: PropTypes.object,

    /**
     * Read-only prop. To use this, make sure that `enableHciEvents` is set to `True`, or that `enableHciEvents` is a list that contains this event type.
     * Fired when the drag has finished.
     */
    dragEnd: PropTypes.object,

    /**
     * Read-only prop. To use this, make sure that `enableHciEvents` is set to `True`, or that `enableHciEvents` is a list that contains this event type.
     * Fired when dragging control node. Control Edge is edge that is being dragged and contains ids of 'from' and 'to' nodes. If control node is not dragged over another node, 'to' field is undefined. Passes an object with properties structured as:
     * {
     *     nodes: [Array of selected nodeIds],
     *     edges: [Array of selected edgeIds],
     *     event: [Object] original click event,
     *     pointer: {
     *         DOM: {x:pointer_x, y:pointer_y},
     *         canvas: {x:canvas_x, y:canvas_y}
     *     },
     *     controlEdge: {from:from_node_id, to:to_node_id}
     * }
     */
    controlNodeDragging: PropTypes.object,

    /**
     * Read-only prop. To use this, make sure that `enableHciEvents` is set to `True`, or that `enableHciEvents` is a list that contains this event type.
     * Fired when the control node drag has finished.
     */
    controlNodeDragEnd: PropTypes.object,

    /**
     * Read-only prop. To use this, make sure that `enableHciEvents` is set to `True`, or that `enableHciEvents` is a list that contains this event type.
     * Fired if the option interaction:{hover:true} is enabled and the mouse hovers over a node.
     */
    hoverNode: PropTypes.object,

    /**
     * Read-only prop. To use this, make sure that `enableHciEvents` is set to `True`, or that `enableHciEvents` is a list that contains this event type.
     * Fired if the option interaction:{hover:true} is enabled and the mouse moved away from a node it was hovering over before.
     */
    blurNode: PropTypes.object,

    /**
     * Read-only prop. To use this, make sure that `enableHciEvents` is set to `True`, or that `enableHciEvents` is a list that contains this event type.
     * Fired if the option interaction:{hover:true} is enabled and the mouse hovers over an edge.
     */
    hoverEdge: PropTypes.object,

    /**
     * Read-only prop. To use this, make sure that `enableHciEvents` is set to `True`, or that `enableHciEvents` is a list that contains this event type.
     * Fired if the option interaction:{hover:true} is enabled and the mouse moved away from an edge it was hovering over before.
     */
    blurEdge: PropTypes.object,

    /**
     * Read-only prop. To use this, make sure that `enableHciEvents` is set to `True`, or that `enableHciEvents` is a list that contains this event type.
     * Fired when the user zooms in or out. The properties tell you which direction the zoom is in. The scale is a number greater than 0, which is the same that you get with network.getScale(). When fired by clicking the zoom in or zoom out navigation buttons, the pointer property of the object passed will be null. Passes an object with properties structured as:
     * {
     *   direction: '+'/'-',
     *   scale: Number,
     *   pointer: {x:pointer_x, y:pointer_y}
     * }
     */
    zoom: PropTypes.object,

    /**
     * Read-only prop. To use this, make sure that `enableHciEvents` is set to `True`, or that `enableHciEvents` is a list that contains this event type.
     * Fired when the popup (tooltip) is shown.
     * Returns id of item corresponding to popup
     */
    showPopup: PropTypes.number,

    /**
     * Read-only prop. To use this, make sure that `enableHciEvents` is set to `True`, or that `enableHciEvents` is a list that contains this event type.
     * Fired when the popup (tooltip) is hidden.
     * Returns none
     */
    hidePopup: PropTypes.number,

    /**
     * Either a boolean indicating if all event callbacks triggered the physics simulation should be enabled,
     * or a list of strings
     * indicating which ones should be used. If it's a list, you will need to specify one of the
     * following events: `startStabilizing`, `stabilizationProgress`, `stabilizationIterationsDone`, `stabilized`.
     * See https://visjs.github.io/vis-network/docs/network/#events for more details.
     */
    enablePhysicsEvents: PropTypes.oneOfType([
        PropTypes.arrayOf(PropTypes.string), PropTypes.bool
    ]),

    /**
     * Read-only prop. To use this, make sure that `enablePhysicsEvents` is set to `True`, or that `enablePhysicsEvents`
     * is a list that contains this event type.
     * Fired when stabilization starts.
     * This is also the case when you drag a node and the physics simulation restarts to stabilize again.
     * Stabilization does not necessarily imply 'without showing'.
     */
    startStabilizing: PropTypes.any,

    /**
     * Read-only prop. To use this, make sure that `enablePhysicsEvents` is set to `True`, or that `enablePhysicsEvents`
     * is a list that contains this event type.
     * Fired when a multiple of the updateInterval number of iterations is reached. This only occurs in the 'hidden'
     * stabilization. Passes an object with properties structured as:
     * {
     *   iterations: Number // iterations so far,
     *   total: Number      // total iterations in options
     * }
     */
    stabilizationProgress: PropTypes.object,

    /**
     * Read-only prop. To use this, make sure that `enablePhysicsEvents` is set to `True`, or that `enablePhysicsEvents`
     * is a list that contains this event type.
     * Fired when the 'hidden' stabilization finishes.
     * This does not necessarily mean the network is stabilized;
     * it could also mean that the amount of iterations defined in the options has been reached.
     */
    stabilizationIterationsDone: PropTypes.any,

    /**
     * Read-only prop. To use this, make sure that `enablePhysicsEvents` is set to `True`, or that `enablePhysicsEvents`
     * is a list that contains this event type.
     * Fired when the network has stabilized or when the stopSimulation() has been called. The amount of iterations it
     * took could be used to tweak the maximum amount of iterations needed to stabilize the network. Passes an object
     * with properties structured as:
     * {
     *   iterations: Number // iterations it took
     * }
     */
    stabilized: PropTypes.object,

    /**
     * Either a boolean indicating if all event callbacks triggered the canvas, rendering, view and configuration
     * modules should be enabled, or a list of strings
     * indicating which ones should be used. If it's a list, you will need to specify one of the
     * following events: `resize`, `initRedraw`, `beforeDrawing`, `afterDrawing`, `animationFinished`,
     * `configChange`.
     * See https://visjs.github.io/vis-network/docs/network/#events for more details.
     */
    enableOtherEvents: PropTypes.oneOfType([
        PropTypes.arrayOf(PropTypes.string), PropTypes.bool
    ]),

    /**
     * Read-only prop. To use this, make sure that `enableOtherEvents` is set to `True`, or that `enableOtherEvents` is
     * a list that contains this event type.
     * Fired when the size of the canvas has been resized, either by a redraw call when the container div has changed
     * in size, a setSize() call with new values or a setOptions() with new width and/or height values. Passes an object
     * with properties structured as:
     * {
     *   width: Number     // the new width  of the canvas
     *   height: Number    // the new height of the canvas
     *   oldWidth: Number  // the old width  of the canvas
     *   oldHeight: Number // the old height of the canvas
     * }
     */
    resize: PropTypes.object,

    /**
     * Read-only prop. To use this, make sure that `enableOtherEvents` is set to `True`, or that `enableOtherEvents` is
     * a list that contains this event type.
     * Fired before the redrawing begins. The simulation step has completed at this point. Can be used to move custom
     * elements before starting drawing the new frame.
     */
    initRedraw: PropTypes.object,

    /**
     * Read-only prop. To use this, make sure that `enableOtherEvents` is set to `True`, or that `enableOtherEvents` is
     * a list that contains this event type.
     *    Fired after the canvas has been cleared, scaled and translated to the viewing position but before all edges
     *    and nodes are drawn. Can be used to draw behind the network.
     */
    beforeDrawing: PropTypes.object,

    /**
     * Read-only prop. To use this, make sure that `enableOtherEvents` is set to `True`, or that `enableOtherEvents` is
     * a list that contains this event type.
     * Fired after drawing on the canvas has been completed. Can be used to draw on top of the network.
     */
    afterDrawing: PropTypes.object,

    /**
     * Read-only prop. To use this, make sure that `enableOtherEvents` is set to `True`, or that `enableOtherEvents`
     * is a list that contains this event type.
     * Fired when an animation is finished.
     */
    animationFinished: PropTypes.object,

    /**
     * Read-only prop. To use this, make sure that `enableOtherEvents` is set to `True`, or that `enableOtherEvents`
     * is a list that contains this event type.
     * Fired when a user changes any option in the configurator.
     * The options object can be used with the setOptions method or stringified using JSON.stringify().
     * You do not have to manually put the options into the network: this is done automatically. You can use the event
     * to store user options in the database.
     */
    configChange: PropTypes.object,

    /** Global methods for the network */
    /** Write-only property. Pass true value to this property as an output to call the underlying function on the graph.
     * Remove the network from the DOM and remove all Hammer bindings and references.
     * Returns: None
     */
    destroy: PropTypes.bool,

    /** setData and setOptions are available through data and options properties respectively **/

    /** Write-only property. Pass true value to this property as an output to call the underlying function on the graph.
     * Set an event listener. Depending on the type of event you get different parameters for
     * the callback function. Look at the event section of the documentation for more information.
     * callback must contain a valid javascript function
     * Returns: None
     */
    on: PropTypes.exact({
        event_name: PropTypes.string,
        callback: PropTypes.string
    }),

    /** Write-only property. Pass true value to this property as an output to call the underlying function on the graph.
     * Remove an event listener.
     * The function you supply has to be the exact same as the one you used in the on function.
     * If no function is supplied, all listeners will be removed.
     * Look at the event section of the documentation for more information.
     * Returns: None
     */
    off: PropTypes.exact({
        event_name: PropTypes.string,
        callback: PropTypes.string
    }),

    /** Write-only property. Pass true value to this property as an output to call the underlying function on the graph.
     * Set an event listener only once. After it has taken place, the event listener will be removed.
     * Depending on the type of event you get different parameters for the callback function.
     * Look at the event section of the documentation for more information.
     * Returns: None
     */
    once: PropTypes.exact({
        event_name: PropTypes.string,
        callback: PropTypes.string
    }),


    /** Canvas methods */
    /** Function call. Pass your values into this property and read off the results from the same property.
     * This function converts canvas coordinates to coordinate on the DOM.
     * Input and output are in the form of {x:Number,y:Number}.
     * The DOM values are relative to the network container. */
    canvasToDOM: PropTypes.exact(
        {
            x: PropTypes.number,
            y: PropTypes.number
        }
    ),

    /** Function call. Pass your values into this property and read off the results from the same property.
     * This function converts DOM coordinates to coordinate on the canvas.
     * Input and output are in the form of {x:Number,y:Number}.
     * The DOM values are relative to the network container. */
    DOMtoCanvas: PropTypes.exact(
        {
            x: PropTypes.number,
            y: PropTypes.number
        }
    ),

    /** Write-only property. Pass true value to this property as an output to call the underlying function on the graph.
     * Redraw the network.
     * Returns: None
     */
    redraw: PropTypes.bool,

    /** Write-only property. Pass true value to this property as an output to call the underlying function on the graph.
     * Set the size of the canvas. This is automatically done on a window resize.
     * Returns: None
     */
    setSize: PropTypes.exact({
        width: PropTypes.string,
        height: PropTypes.string
    }),

    /** Clustering methods */
    /** Function call. Returns nothing.
     * 	Clusters the network according to the passed in options.
     * 	The options object is explained in full below. The joinCondition function is presented with all nodes. */
    cluster: PropTypes.exact({
        options: ClusteringOptions,
    }),

    /** Function call. Returns nothing.
     * This method looks at the provided node and makes a cluster of it and all it's connected nodes.
     * The behaviour can be customized by proving the options object. All options of this object are explained below.
     * The joinCondition is only presented with the connected nodes. */
    clusterByConnection: PropTypes.exact({
        nodeId: PropTypes.string,
        options: ClusteringOptions
    }),

    /** Function call. Returns nothing.
     * This method checks all nodes in the network and those with a equal or higher amount of edges than
     * specified with the hubsize qualify. If a hubsize is not defined, the hubsize will be determined
     * as the average value plus two standard deviations.
     *
     * For all qualifying nodes, clusterByHubsize is performed on each of them.
     * The options object is described for clusterByHubsize and does the same here. */
    clusterByHubsize: PropTypes.exact({
        hubsize: PropTypes.number,
        options: ClusteringOptions
    }),

    /** Function call. Returns nothing.
     *  This method will cluster all nodes with 1 edge with their respective connected node.
     *  The options object is explained in full below. */
    clusterOutliers: PropTypes.exact({
        options: ClusteringOptions,
    }),

    /** Function call. Returns array of node ids showing in which clusters the desired node id exists in (if any).
     *  Nodes can be in clusters. Clusters can also be in clusters.
     *  This function returns and array of nodeIds showing where the node is.
     * If any nodeId in the chain, especially the first passed in as a parameter,
     * is not present in the current nodes list, an empty array is returned.
     *
     * Example: cluster 'A' contains cluster 'B', cluster 'B' contains cluster 'C', cluster 'C' contains node 'fred'.
     * network.clustering.findNode('fred') will return ['A','B','C','fred'].*/
    findNode: PropTypes.shape({
        nodeId: PropTypes.oneOfType([PropTypes.string, PropTypes.number]),
        result: PropTypes.arrayOf(PropTypes.string),
    }),

    /** Function call.
     * Similar to findNode in that it returns all the edge ids that were
     * created from the provided edge during clustering.
     * Check the result property for results of this function call. */
    getClusteredEdges: PropTypes.shape({
        baseEdgeId: PropTypes.string,
        result: PropTypes.arrayOf(PropTypes.string),
    }),

    /** Function call.
     * For the given clusteredEdgeId, this method will return all the original base edge id's provided in data.edges.
     * For a non-clustered (i.e. 'base') edge, clusteredEdgeId is returned.
     *
     * Only the base edge id's are returned. All clustered edges id's under clusteredEdgeId are skipped,
     * but scanned recursively to return their base id's. */
    getBaseEdges: PropTypes.shape({
        clusteredEdgeId: PropTypes.string,
        result: PropTypes.arrayOf(PropTypes.string),
    }),

    /** Function call. Returns nothing.
     * Visible edges between clustered nodes are not the same edge as the ones provided in data.edges passed on network creation
     * With each layer of clustering, copies of the edges between clusters are created and the previous edges are hidden, until the cluster is opened.
     * This method takes an edgeId (ie. a base edgeId from data.edges) and applies the options to it and any edges that were created from it while clustering.
     *
     * Example: network.clustering.updateEdge(originalEdge.id, {color : '#aa0000'});
     * This would turn the base edge and any subsequent edges red, so when opening clusters the edges will all be the same color. */
    updateEdge: PropTypes.exact({
        startEdgeId: PropTypes.string,
        options: PropTypes.object
    }),

    /** Function call. Returns nothing.
     * Visible edges between clustered nodes are not the same edge as the ones provided in data.edges passed on network creation
     * With each layer of clustering, copies of the edges between clusters are created and the previous edges are hidden, until the cluster is opened.
     * This method takes an edgeId (ie. a base edgeId from data.edges) and applies the options to it and any edges that were created from it while clustering.
     *
     * Example: network.clustering.updateEdge(originalEdge.id, {color : '#aa0000'});
     * This would turn the base edge and any subsequent edges red, so when opening clusters the edges will all be the same color. */
    updateClusteredNode: PropTypes.exact({
        clusteredNodeId: PropTypes.string,
        options: PropTypes.object
    }),

    /** Function call. Returns true if the node whose ID has been supplied is a cluster. */
    isCluster: PropTypes.shape({
        nodeId: PropTypes.string,
        result: PropTypes.bool,
    }),

    /** Function call. Returns an array of all nodeIds of the nodes that would be released if you open the cluster. */
    getNodesInCluster: PropTypes.shape({
        clusteredNodeId: PropTypes.string,
        result: PropTypes.arrayOf(PropTypes.string),
    }),

    /** Function call.
     * Opens the cluster, releases the contained nodes and edges, removing the cluster node and cluster edges.
     * The options object is optional and currently supports one option, releaseFunction, which is a function that can be used to manually position the nodes after the cluster is opened.
     * function releaseFunction (clusterPosition, containedNodesPositions) {
     *     var newPositions = {};
     *     // clusterPosition = {x:clusterX, y:clusterY};
     *     // containedNodesPositions = {nodeId:{x:nodeX,y:nodeY}, nodeId2....}
     *     newPositions[nodeId] = {x:newPosX, y:newPosY};
     *     return newPositions;
     * }
     * The containedNodesPositions contain the positions of the nodes in the cluster at the moment they were clustered.
     * This function is expected to return the newPositions, which can be the containedNodesPositions (altered) or
     * a new object. This has to be an object with keys equal to the nodeIds that exist in the containedNodesPositions
     * and an {x:x,y:y} position object.
     *
     * For all nodeIds not listed in this returned object, we will position them at the location of the cluster.
     * This is also the default behaviour when no releaseFunction is defined. */
    openCluster: PropTypes.shape({
        nodeId: PropTypes.string,
        options: PropTypes.object
    }),

    /** Layout methods */
    /**
     * Read-only prop.
     * If you like the layout of your network and would like it to start in the same way next time, ask for the seed using this method and put it in the layout.randomSeed option.
     */
    getSeed: PropTypes.oneOfType([PropTypes.string, PropTypes.number]),

    /** Manipulation methods */
    /** Write-only property. Pass true value to this property as an output to call the underlying function on the graph.
     * Programmatically enable the edit mode. Similar effect to pressing the edit button.
     * Returns: None
     */
    enableEditMode: PropTypes.bool,

    /** Write-only property. Pass true value to this property as an output to call the underlying function on the graph.
     * Programmatically disable the edit mode. Similar effect to pressing the close icon (small cross in the corner of the toolbar).
     * Returns: None
     */
    disableEditMode: PropTypes.bool,

    /** Write-only property. Pass true value to this property as an output to call the underlying function on the graph.
     * Go into addNode mode. Having edit mode or manipulation enabled is not required.
     * To get out of this mode, call disableEditMode().
     * The callback functions defined in handlerFunctions still apply.
     * To use these methods without having the manipulation GUI, make sure you set enabled to false.
     * Returns: None
     */
    addNodeMode: PropTypes.bool,

    /** Write-only property. Pass true value to this property as an output to call the underlying function on the graph.
     * Edit the selected node. The explanation from addNodeMode applies here as well.
     * Returns: None
     */
    editNode: PropTypes.bool,

    /** Write-only property. Pass true value to this property as an output to call the underlying function on the graph.
     * Go into addEdge mode. The explanation from addNodeMode applies here as well.
     * Returns: None
     */
    addEdgeMode: PropTypes.bool,

    /** Write-only property. Pass true value to this property as an output to call the underlying function on the graph.
     * Go into editEdge mode. The explanation from addNodeMode applies here as well.
     * Returns: None
     */
    editEdgeMode: PropTypes.bool,

    /** Write-only property. Pass true value to this property as an output to call the underlying function on the graph.
     * Delete selected. Having edit mode or manipulation enabled is not required.
     * Returns: None
     */
    deleteSelected: PropTypes.bool,

    /** Methods to get information on nodes and edges */

    /** Function call.
     * Returns the x y positions in canvas space of the nodes or node with the supplied nodeIds or nodeId as an object:
     * // All nodes in the network.
     * network.getPositions();
     * >   {
     *         a123: { x: 5, y: 12 },
     *         b456: { x: 3, y: 4 },
     *         c789: { x: 7, y: 10 }
     *     }
     *
     *
     * // Specific nodes.
     * network.getPositions(['a123', 'b456']);
     * >   {
     *         a123: { x: 5, y: 12 },
     *         b456: { x: 3, y: 4 },
     *     }
     *
     *
     * // A single node.
     * network.getPositions('a123');
     * >   {
     *         a123: { x: 5, y: 12 }
     *     }
     *
     *
     * Alternative inputs are a string containing a nodeId or nothing. When a string is supplied, the position of the node corresponding to the id is returned in the same format. When nothing is supplied, the positions of all nodes are returned.
     * Note: If a non-existent id is supplied, the method will return an empty object. */
    getPositions: PropTypes.shape({
        nodeIds: PropTypes.array,
        result: PropTypes.object,
    }),

    /** Function call.
     * Returns the x y positions in canvas space of a specific node.
     * network.getPosition('a123');
     * >   { x: 5, y: 12 }
     *
     * If no id is provided, the method will throw a TypeError
     * If an id is provided that does not correspond to a node in the network, the method will throw a ReferenceError. */
    getPosition: PropTypes.shape({
        nodeId: PropTypes.string,
        result: PropTypes.object,
    }),

    /** Write-only property. Pass true value to this property as an output to call the underlying function on the graph.
     * When using the vis.DataSet to load your nodes into the network, this method will put the X and Y positions of all nodes into that dataset. If you're loading your nodes from a database and have this dynamically coupled with the DataSet, you can use this to stabilize your network once, then save the positions in that database through the DataSet so the next time you load the nodes, stabilization will be near instantaneous.
     *
     * If the nodes are still moving and you're using dynamic smooth edges (which is on by default), you can use the option stabilization.onlyDynamicEdges in the physics module to improve initialization time.
     *
     * This method does not support clustering. At the moment it is not possible to cache positions when using clusters since they cannot be correctly initialized from just the positions.
     *  moveNode(nodeId, Number x, Number y)
     *  getBoundingBox(String nodeId)
     *  getConnectedNodes(String nodeId or edgeId, [String direction])
     *  getConnectedEdges(String nodeId)
     * Returns: None
     */
    storePositions: PropTypes.bool,

    /** Function call.
     * You can use this to programmatically move a node. The supplied x and y positions have to be in canvas space! */
    moveNode: PropTypes.shape({
        nodeId: PropTypes.string,
        x: PropTypes.number,
        y: PropTypes.number,
    }),

    /** Function call.
     * Returns a bounding box for the node including label in the format:
     * {
     *   top: Number,
     *   left: Number,
     *   right: Number,
     *   bottom: Number
     * }
     * These values are in canvas space. */
    getBoundingBox: PropTypes.shape({
        nodeId: PropTypes.string,
        result: PropTypes.object,
    }),

    /** Function call.
     * Returns an array of nodeIds of all the nodes that are directly connected to this node or edge.
     *
     * For a node id, returns an array with the id's of the connected nodes.
     * If optional parameter direction is set to string 'from', only parent nodes are returned.
     * If direction is set to 'to', only child nodes are returned.
     * Any other value or undefined returns both parent and child nodes.
     *
     * For an edge id, returns an array: [fromId, toId]. Parameter direction is ignored for edges. */
    getConnectedNodes: PropTypes.shape({
        nodeId: PropTypes.string,
        direction: PropTypes.string,
        result: PropTypes.arrayOf(PropTypes.number),
    }),

    /** Function call.
     * Returns an array of edgeIds of the edges connected to this node. */
    getConnectedEdges: PropTypes.shape({
        nodeId: PropTypes.string,
        result: PropTypes.arrayOf(PropTypes.string),
    }),

    /** Physics methods to control when the simulation should run */
    /** Function call.
     * Start the physics simulation. This is normally done whenever needed and is only really useful
     * if you stop the simulation yourself and wish to continue it afterwards. */
    startSimulation: PropTypes.bool,

    /** Function call.
     * Returns a bounding box for the node including label in the format:
     * {
     *   top: Number,
     *   left: Number,
     *   right: Number,
     *   bottom: Number
     * }
    * These values are in canvas space. */
    stopSimulation: PropTypes.bool,

    /** Function call.
     * You can manually call stabilize at any time. All the stabilization options above are used.
     * You can optionally supply the number of iterations it should do. */
    stabilize: PropTypes.number,

    /** Selection methods for nodes and edges. */
    /** Read-only property.
     * Returns an object with selected nodes and edges ids like this:
     * {
     *   nodes: [Array of selected nodeIds],
     *   edges: [Array of selected edgeIds]
     * } */
    getSelection: PropTypes.object,

    /** Read-only property.
     * Returns an array of selected node ids like so: [nodeId1, nodeId2, ..]. */
    getSelectedNodes: PropTypes.arrayOf(PropTypes.oneOfType([PropTypes.string, PropTypes.number])),

    /** Read-only property.
     * Returns an array of selected edge ids like so: [edgeId1, edgeId2, ..]. */
    getSelectedEdges: PropTypes.arrayOf(PropTypes.oneOfType([PropTypes.string, PropTypes.number])),

    /** Function call.
     * Returns a nodeId or undefined.
     * The DOM positions are expected to be in pixels from the top left corner of the canvas. */
    getNodeAt: PropTypes.shape({
        position: PropTypes.exact({
            x: PropTypes.number,
            y: PropTypes.number,
        }),
        result: PropTypes.arrayOf(PropTypes.string),
    }),

    /** Function call.
     * Returns an edgeId or undefined.
     * The DOM positions are expected to be in pixels from the top left corner of the canvas. */
    getEdgeAt: PropTypes.shape({
        position: PropTypes.exact({
            x: PropTypes.number,
            y: PropTypes.number,
        }),
        result: PropTypes.arrayOf(PropTypes.string),
    }),

    /** Function call.
     * Selects the nodes corresponding to the id's in the input array.
     * If highlightEdges is true or undefined, the neighbouring edges will also be selected.
     * This method unselects all other objects before selecting its own objects.
     * Does not fire events. */
    selectNodes: PropTypes.shape({
        nodeIds: PropTypes.array,
        highlightEdges: PropTypes.bool,
    }),

    /** Function call.
     * Selects the edges corresponding to the id's in the input array.
     * This method unselects all other objects before selecting its own objects.
     * Does not fire events.*/
    selectEdges: PropTypes.shape({
        edgeIds: PropTypes.array,
    }),

    /** Function call.
     * Sets the selection, wich must be an object like this:
     * {
     *   nodes: [Array of nodeIds],
     *   edges: [Array of edgeIds]
     * }
     * You can also pass only nodes or edges in selection object. Available options are:
     * {
     *   unselectAll: Boolean,
     *   highlightEdges: Boolean
     * }*/
    setSelection: PropTypes.shape({
        selection: PropTypes.exact({
            nodes: PropTypes.arrayOf(PropTypes.string),
            edges: PropTypes.arrayOf(PropTypes.string),
        }),
        options: PropTypes.shape({
            unselectAll: PropTypes.bool,
            highlightEdges: PropTypes.bool,
        })
    }),

    /** Function call.
     * Unselect all objects. Does not fire events. */
    unselectAll: PropTypes.bool,

    /** Methods to control the viewport for zoom and animation. */
    /** Read-only property.
     * Returns the current scale of the network.
     * 1.0 is comparable to 100%, 0 is zoomed out infinitely.
     */
    getScale: PropTypes.number,

    /** Read-only property.
     * Returns the current central focus point of the view in the form: { x: {Number}, y: {Number} }
     */
    getViewPosition: PropTypes.shape({
        x: PropTypes.number,
        y: PropTypes.number,
    }),

    /** Function call.
     * You can focus on a node with this function. What that means is the view will lock onto that node,
     * if it is moving, the view will also move accordingly. If the view is dragged by the user, the focus is broken.
     * You can supply options to customize the effect:
     * {
     *   scale: Number,
     *   offset: {x:Number, y:Number}
     *   locked: boolean
     *   animation: { // -------------------> can be a boolean too!
     *     duration: Number
     *     easingFunction: String
     *   }
     * }
     * All options except for locked are explained in the moveTo() description below.
     * Locked denotes whether or not the view remains locked to the node once the zoom-in animation is finished.
     * Default value is true. The options object is optional in the focus method.
     */
    focus: PropTypes.shape({
        nodeId: PropTypes.string,
        options: FocusOptions,
    }),

    /** Function call.
     * You can animate or move the camera using the moveTo method. Options are:
     * {
     *   position: {x:Number, y:Number},
     *   scale: Number,
     *   offset: {x:Number, y:Number}
     *   animation: { // -------------------> can be a boolean too!
     *     duration: Number
     *     easingFunction: String
     *   }
     * }
     * The position (in canvas units!) is the position of the central focus point of the camera.
     * The scale is the target zoomlevel. Default value is 1.0. The offset (in DOM units) is how many pixels from the
     * center the view is focussed. Default value is {x:0,y:0}. For animation you can either use a Boolean to use it
     * with the default options or disable it or you can define the duration (in milliseconds) and easing function
     * manually. Available are: linear, easeInQuad, easeOutQuad, easeInOutQuad, easeInCubic, easeOutCubic,
     * easeInOutCubic, easeInQuart, easeOutQuart, easeInOutQuart, easeInQuint, easeOutQuint, easeInOutQuint.
     * You will have to define at least a scale, position or offset. Otherwise, there is nothing to move to.
     */
    moveTo: PropTypes.shape({
        options: MoveToOptions,
    }),

    fit: PropTypes.shape({
        options: FitOptions,
    }),

    /** Function call.
     * Programmatically release the focussed node.
     */
    releaseNode: PropTypes.bool,

    /** Methods to use with the configurator module. */
    /** Function call.
     * If you use the configurator, you can call this method to get an options object that contains all differences
     * from the default options caused by users interacting with the configurator.
     */
    getOptionsFromConfigurator: PropTypes.object,

    /**
     * Dash-assigned callback that should be called to report property changes
     * to Dash, to make them available for callbacks.
     */
    setProps: PropTypes.func,

};
DashNetwork.defaultProps = {
    data: {
        nodes: [{id: 1, cid: 1, label: 'Node 1', title: 'This is Node 1'},
            {id: 2, cid: 1, label: 'Node 2', title: 'This is Node 2'},
            {id: 3, cid: 1, label: 'Node 3', title: 'This is Node 3'},
            {id: 4, label: 'Node 4', title: 'This is Node 4'},
            {id: 5, label: 'Node 5', title: 'This is Node 5'}],
        edges: [{from: 1, to: 3},
            {from: 1, to: 2},
            {from: 2, to: 4},
            {from: 2, to: 5}]
    },
    options: {},
    afterDrawing: {},
    enableHciEvents: false,
    enablePhysicsEvents: false,
    enableOtherEvents: false,
    enableEditMode: false,
    destroy: false,
    redraw: false,
    canvasToDOM: null,
    DOMtoCanvas: null,
    cluster: null,
    clusterByConnection: null,
    setSize: {},
    getPosition: null,
    getPositions: null,
    getBoundingBox: null,
    getConnectedEdges: null,
    getConnectedNodes: null,
    moveNode: null,
    startSimulation: null,
    stopSimulation: null,
    stabilize: null,
};