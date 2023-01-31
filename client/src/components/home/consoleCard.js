import TerminalRounded from '@mui/icons-material/TerminalRounded';
import { Avatar, Button, CardHeader, Paper, Typography } from '@mui/material'
import { purple } from '@mui/material/colors';
import React, { Component, useEffect, useState } from 'react'

function ConsoleCard() {
  const [logs, setLogs] = useState([]);

  const fetchLogs = () => {
    fetch("http://<REMOTE IP>:9823/logs?password=<PASSWORD>&remote=True")
      .then((response) => response.json())
      .then((response) => {
        setLogs(response);
      })
      .catch(() => {
        console.log("ERROR");
      });
    }
    return (
        <Paper elevation={3} style={{'background': '#455a64'}}>
        <CardHeader
       style={{'background': '#b0bec5'}}
       avatar={
         <Avatar sx={{ bgcolor: purple[500] }} aria-label="Console">
          <TerminalRounded/>
         </Avatar>
       }
       action={
        <Button variant="contained" onClick={fetchLogs}>
        GET LOGS
      </Button>
      
      }
       title="H A R D W A R E"
       subheader="CONSOLE"
     />
 <Typography component={'span'}> {logs.map(log => <p>{log.message}</p>)}</Typography>
        <br/>
        <br/>
        <br/>
        <br/>
        <br/>
        <br/>
        </Paper>
    )
}

export default ConsoleCard;