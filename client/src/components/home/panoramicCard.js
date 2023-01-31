import { Avatar, Button, CardHeader, IconButton, Paper } from '@mui/material'
import { red } from '@mui/material/colors';
import React, {useState } from 'react'
import CameraswitchRoundedIcon from '@mui/icons-material/CameraswitchRounded';
import VrpanoRoundedIcon from '@mui/icons-material/VrpanoRounded';
import { Pannellum} from "pannellum-react";
import RefreshRoundedIcon from '@mui/icons-material/RefreshRounded';
function PanoCard() {
  const [url, setUrl] = useState("");

  const generatePano = () => {
    fetch("http://<REMOTE IP>:9823/generatepano?password=<PASSWORD>&remote=True")
      .then((response) => response.json())
      .then((response) => {
        console.log(response);
        setUrl("");
      })
      .catch(() => {
        console.log("ERROR");
      });
    }
    
    return (
        <Paper elevation={3} >
        <CardHeader
        style={{'background': '#b0bec5'}}
        avatar={
          <Avatar sx={{ bgcolor: red[500] }} aria-label="Camera">
           <CameraswitchRoundedIcon/>
          </Avatar>
        }
        action={
          <Button variant="contained" startIcon={<VrpanoRoundedIcon />} onClick={generatePano}>
          Panoramic
        </Button>
        
        }
        title="I M A G I N G"
        subheader="PANORAMIC IMAGING"
      />
      
            <div>
              <br/>
        <IconButton aria-label="Refresh" onClick={() => setUrl('http://<REMOTE IP>:9823/panoramic?password=<PASSWORD>&remote=True')}>
        <RefreshRoundedIcon />
        </IconButton>
        <br/>
            <Pannellum
        width="100%"
        height="400px"
        image={url}
        pitch={10}
        yaw={180}
        hfov={110}
        autoLoad
        onLoad={() => {
            console.log("panorama loaded");
        }}
    >
 
    </Pannellum>
            </div>
         <br/>
        
         </Paper>
    )
}

export default PanoCard;