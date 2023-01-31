import Node from "./Djikstra/Node";
import NavigationBar from "./Djikstra/NavigationBar";
import React, { useState, useEffect } from 'react';
import { Button } from "@mui/material";

export default function Main() {
  const [ourRobotX, setOurRobotX] = useState(0);
  const [ourRobotY, setOurRobotY] = useState(0);
  const [rawMap, setRawMap]  = useState([]);
  const [grid, setGrid] = useState([]);
  const [path, setPath] = useState([]);
  const [djikstraPost, setDjikstraPost] = useState({});

var FINISH_NODE_ROW = 1;
var FINISH_NODE_COL = 7;

const [intervalId, setIntervalId] = useState(0);

var myHeaders = new Headers();
myHeaders.append("Content-Type", "application/json");
myHeaders.append("Cookie", "session=468bd4d8-d02e-4d26-a2ef-1849dc4aff3f");
myHeaders.append("Access-Control-Allow-Origin", "*");

var raw = JSON.stringify(djikstraPost);

var requestOptions = {
  method: 'POST',
  headers: myHeaders,
  body: raw,
  redirect: 'follow'
};

const postDjikstra = () =>  {
  fetch("http://<REMOTE IP>:9823/autonomous?password=<PASSWORD>&remote=True", requestOptions)
  .then(response => response.text())
  .then(result => console.log(result))
  .catch(error => console.log('error', error));
}
const clearObstacles = () =>  {
  fetch("http://<REMOTE IP>:9823/clear_obstacles?password=<PASSWORD>&remote=True")
  .then(response => response.text())
  .then(result => console.log(result))
  .catch(error => console.log('error', error));
}

 const fetchMap = () => {
  fetch("http://<REMOTE IP>:9823/mapdata?password=<PASSWORD>&remote=True")
    .then((response) => response.json())
    .then((response) => {
      for (let i = 0; i < response.length; i++) {
        setRawMap(response)
        if(response[i].object_type == "OurRobot"){
          setOurRobotX(response[i].location[0])
          setOurRobotY(response[i].location[1])
        }
        
      }
    }).then(setGrid(getObstacleGrid(rawMap)))
    .catch(() => {
      console.log("ERROR");
    });
  }
  const getData = () => {
    if(intervalId) {
      clearInterval(intervalId);
      setIntervalId(0);
      return;
    }
    const timerId = setInterval(() => {
      fetchMap();
      console.log('Successful Location GET');
    }, 5000);
    setIntervalId(timerId);
    
  }
  const getInitialGrid = () => {
    const grid = [];
    for (let row = 0; row < 11; row++) {
      const currentRow = [];
      for (let col = 0; col < 11; col++) {
        currentRow.push(createNode(col, row));
      }
      grid.push(currentRow);
    }
    return grid;
  };
  const getObstacleGrid = (rawMap) => {
    const grid = [];
    for (let row = 0; row < 11; row++) {
      const currentRow = [];
      for (let col = 0; col < 11; col++) {
        currentRow.push(createNode(col, row));
      }
      grid.push(currentRow);
    }
    console.log(rawMap)
    for (let i = 0; i < rawMap.length ; i++) {
        const newGrid = getNewGridWithWallToggled(grid, rawMap[i].location[0], rawMap[i].location[1]);
    setGrid(newGrid);
      
    }
    return grid;
  };
  const createNode = (col, row) => {
    return {
      col,
      row,
      isStart: row === ourRobotX && col === ourRobotY,
      isFinish: row === FINISH_NODE_ROW && col === FINISH_NODE_COL,
      distance: Infinity,
      isVisited: false,
      isWall: false,
      previousNode: null
    };
  };
 
  useEffect(() => {
    setGrid(getInitialGrid())
  }, []);
 
  function animateDijkstra(visitedNodesInOrder, nodesInShortestPathOrder) {
    for (let i = 0; i <= visitedNodesInOrder.length; i++) {
      if (i === visitedNodesInOrder.length) {
        setTimeout(() => {
          animateShortestPath(nodesInShortestPathOrder);
        }, 11 * i);
        return;
      }
      setTimeout(() => {
        const node = visitedNodesInOrder[i];
        document.getElementById(`node-${node.row}-${node.col}`).className =
          "node node-visited";
      }, 11 * i);
    }
  }

  function animateShortestPath(nodesInShortestPathOrder) {
    for (let i = 0; i < nodesInShortestPathOrder.length; i++) {
      setTimeout(() => {
        const node = nodesInShortestPathOrder[i];
        document.getElementById(`node-${node.row}-${node.col}`).className =
          "node node-shortest-path";
      }, 50 * i);
    }
  }

  function visualizeDijkstra() {
    const startNode = grid[ourRobotX][ourRobotY];
    const finishNode = grid[FINISH_NODE_ROW][FINISH_NODE_COL];
    const visitedNodesInOrder = dijkstra(grid, startNode, finishNode);
    const nodesInShortestPathOrder = getNodesInShortestPathOrder(finishNode);
    animateDijkstra(visitedNodesInOrder, nodesInShortestPathOrder);
  }

  function clearPath() {
     setGrid(getInitialGrid());
  }
 
  
 
  const getNewGridWithWallToggled = (grid, row, col) => {
    const newGrid = grid.slice();
    const node = newGrid[row][col];
    const newNode = {
      ...node,
      isWall: !node.isWall
    };
    newGrid[row][col] = newNode;
    return newGrid;
  };
  function dijkstra(grid, startNode, finishNode) {
    const visitedNodesInOrder = [];
    startNode.distance = 0;
    const unvisitedNodes = getAllNodes(grid);
    while (!!unvisitedNodes.length) {
      sortNodesByDistance(unvisitedNodes);
      const closestNode = unvisitedNodes.shift();
      // If we encounter a wall, we skip it.
      if (closestNode.isWall) continue;
      // If the closest node is at a distance of infinity,
      // we must be trapped and should therefore stop.
      if (closestNode.distance === Infinity) return visitedNodesInOrder;
      closestNode.isVisited = true;
      visitedNodesInOrder.push(closestNode);
      if (closestNode === finishNode) return visitedNodesInOrder;
      updateUnvisitedNeighbors(closestNode, grid);
    }
  }
  
  function sortNodesByDistance(unvisitedNodes) {
    unvisitedNodes.sort((nodeA, nodeB) => nodeA.distance - nodeB.distance);
  }
  
  function updateUnvisitedNeighbors(node, grid) {
    const unvisitedNeighbors = getUnvisitedNeighbors(node, grid);
    for (const neighbor of unvisitedNeighbors) {
      neighbor.distance = node.distance + 1;
      neighbor.previousNode = node;
    }
  }
  
  function getUnvisitedNeighbors(node, grid) {
    const neighbors = [];
    const { col, row } = node;
    if (row > 0) neighbors.push(grid[row - 1][col]);
    if (row < grid.length - 1) neighbors.push(grid[row + 1][col]);
    if (col > 0) neighbors.push(grid[row][col - 1]);
    if (col < grid[0].length - 1) neighbors.push(grid[row][col + 1]);
    return neighbors.filter(neighbor => !neighbor.isVisited);
  }
  
  function getAllNodes(grid) {
    const nodes = [];
    for (const row of grid) {
      for (const node of row) {
        nodes.push(node);
      }
    }
    return nodes;
  }
  
  // Backtracks from the finishNode to find the shortest path.
  // Only works when called *after* the dijkstra method above.
function getNodesInShortestPathOrder(finishNode) {

  const generateCoordinates = () => {
    setPath(path.reverse())
    setDjikstraPost(
      {
        "Coordinates": path
      }
    )
    console.log({
      "Coordinates": path
    })
    
  }
    const nodesInShortestPathOrder = [];
    let currentNode = finishNode;
    while (currentNode !== null) {
      //ADURAND INSTRUCTIONS
      //console.log('Current Node: COLUMN: ' + currentNode.col + " ROW: "  + currentNode.row)
      path.push([currentNode.col, currentNode.row])
      nodesInShortestPathOrder.unshift(currentNode);
      currentNode = currentNode.previousNode;
    }
    generateCoordinates()
    return nodesInShortestPathOrder;
  }
    return (
      <div>
       

        <div className="grid">
          {grid.map((row, rowIdx) => {
            return (
       
              <div key={rowIdx}>
                {row.map((node, nodeIdx) => {
                  const { row, col, isFinish, isStart, isWall } = node;
                  return (
                    <Node
                      key={nodeIdx}
                      col={col}
                      isFinish={isFinish}
                      isStart={isStart}
                      isWall={isWall}
                      row={row}
                    ></Node>
                  );
                })}
              </div>
             
            );
          })}
        </div>
        <br/>
        <NavigationBar
        style={{zIndex: '2'}}
          onVisiualizePressed={() => visualizeDijkstra()}
          onClearPathPressed={() => clearPath()}
          getCoordinates={() => fetchMap()}
          timeCoordinates={() => getData()}
          postCoordinates={() => postDjikstra()}
          clearObstacles={() => clearObstacles()}
        />
      </div>
    );
  }


