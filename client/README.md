# Getting Started with Robot Radar GUI (Group C)

 

This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app).
<<<<<<< HEAD
In addition, we have implemented the [Material UI](https://mui.com/) frontend component libraries, for each structured card amd icon. The Pannellum library was used for panoramic generation. The radar gui design and Dijkstra visualization was inspired by the open source [Path Finder Visualization Tool](https://github.com/PrudhviGNV/pathFinderVisualizer). Although functionally similiar, the implementation of React functional component and mapping functions were within the bounds of our own project work. 

## How to Use

#### Manual Update Button
This button MUST be clicked twice.

Required after every move command in order to plot the current location of the robot and obstacles in the field. The Forward and Reverse arrow commands are the only commands which collect radar data, therfor, a left or right movement must be followed by a forward or reverse command in order to capture surrounding obstacles and location data.

#### Get Logs Button
Returns a list of all logs, with the most recent rendered at the top of the log card.

#### Generate Panoramic Button
This button sends a POST request to the server indicating that the robot must move and capture images, which are stithced together by the server.

#### Refresh Icon Button
This button retrieves the generated panoramic image. NOTE: The page must be refreshed in order to retrieve a panoramic image 
generated after the first generation.

## Movement Controls
The arrow buttons control basic up, down left, right movement in conjunction with the location where they rest. In addition, there exists an event listener which permits the WASD keyboard controls.

## Radar Functionality

#### Generate Path Button
Generate Path, displays and logs the current block path from the robot to the pre-defined target. One must ALWAYS run the generate path button before the execute path button. 

#### Execute Path Button
Sends the Dijkstra coordinate array to the server.  These are then into physical robot movement commands,
and the robot will move to the pre-defined target.  Due to compounding movement errors, it will likely not end up exactly in that spot.

After this, you must hit the System Reset button

#### System Reset Button
Refreshes the page.  Must be used after Execute Path has been used.  Hit Manual Update button twice to refresh the grid.
The robot will not show up as it is currently at the target button - move it and it will show again after a Manual Update.

## Use Sequence

Runs the app if and only if the robot is on. 
Open [Robot Radar Client](http://<REMOTE IP>:36001/home) to view it in your browser.


## Running locally

Remember to cd into the client directory before trying to run the app.

Use `npm start` to start the app.

## Building to Docker & Deployment

Run `docker build -t robot-radar-client .` to build the docker image.

To run the container ensure that the port mapping maps the local host port `3000` to the desired target port.

The following command encompasses the required instructions. 

`docker run -dp 36000:3000 robot-radar-client`

#### Deploying to remote General Instructions
Save your image on your local machine:
`docker save robot-radar-client > robot-radar-client.tar`
Upload tar to your remote server:
`scp robot-radar-client.tar user@<REMOTE IP>:.`
Load image on your remote machine:
`ssh user@<REMOTE IP>`
`docker load < robot-radar-client.tar`

Run a new container

`docker run -dp 36000:3000 robot-radar-client`



=======
In addition, we have implimented the [Material UI](https://mui.com/) frontend component libraries, for each structured card amd icon. The Pannellum library was used for panoramic generation. The radar gui design and djikstra visualization was inspired by the open source [Path Finder Visualization Tool](https://github.com/PrudhviGNV/pathFinderVisualizer). Although functionally similiar, the implimentation of react functional components, and mapping functions were within the bounds of our own project work. 

## How to Use

#### Get Logs Button
Returns a list of all logs, with the most recent rendered at the top of the log card.

#### Generate Panoramic Button
This button sends a POST request to the server indicating that the robot must move and capture images, which are stithced together by the server.

#### Refresh Icon Button
This button retrieves the generated Panormaic image. NOTE: The page must refresh in order to re-send a panoramic image request.

## Movement Controls
The arrow buttons control basic up, down left, right movement in conjunction with the location where they rest. In addition, there exists an event lister which permits the WASD keyboard controls.

## Radar Functionality

#### Refresh Button
This button clears the field after a a djikstra visualization occurs.

#### Manual Update Button
This button is required after every move command in order to plot the current location of the robot and obstacles in the field. The Forward and Reverse arrow commands are the only commands which collect radar data, therfor, a left or right movement must be followed by a forward or reverse command in order to capture surrounding obstacles and location data.

#### Generate Path Button
Generate Path, displays and logs the current block path from the robot to the target. One must ALWAYS run the generate path button before the execute path button. 

#### Execute Path Button
This button send the Djikstra coordinate array to the server which translate them into physical robot movement commands. 

## Use Sequence

Runs the app if and only if the robot is on. 
Open [Robot Radar Client](http://<REMOTE IP>:36001/home) to view it in your browser.


## Running locally

***Remember to cd into the client directory before trying to run the app.
use `npm start` to start the app.

## Building to Docker & Deployment

Run `docker build -t robot-radar-client .` to build the docker image.

To run the container ensure that the port mapping maps the local host port `3000` to the desired target port.

The following command encompasses the required instructions. 

`docker run -dp 36000:3000 robot-radar-client`

#### Deploying to remote General Instructions
Save your image on your local machine:
`docker save robot-radar-client > robot-radar-client.tar`
Upload tar to your remote server:
`scp robot-radar-client.tar user@<REMOTE IP>:.`
Load image on your remote machine:
`ssh user@<REMOTE IP>`
`docker load < obot-radar-client.tar`

Run a new container

`docker run -dp 36000:3000 robot-radar-client`



>>>>>>> c22702c (Post deployment: Updated ReadME)
