import RadarRounded from '@mui/icons-material/RadarRounded';
import { Avatar, CardHeader, Paper } from '@mui/material'
import { blue } from '@mui/material/colors';
import React, { Component } from 'react'
import Main from '../Main/Main';

function RadarCard() {
 
    return (
        <Paper elevation={3}>
        <CardHeader
       style={{'background': '#b0bec5'}}
       avatar={
         <Avatar sx={{ bgcolor: blue[500] }} aria-label="Radar">
          <RadarRounded/>
         </Avatar>
       }
       title="R A D A R"
       subheader="PATHFINDER"
     />
        <br/>
        <Main/>
        </Paper>
    )
}

export default RadarCard;