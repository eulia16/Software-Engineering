import * as React from 'react';
import Box from '@mui/material/Box';
import Card from '@mui/material/Card';
import CardActions from '@mui/material/CardActions';
import CardContent from '@mui/material/CardContent';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import { Icon } from '@mui/material';
import InfoRoundedIcon from '@mui/icons-material/InfoRounded';


export default function InfoCard() {
  return (
    <Card sx={{ maxWidth: 500, backgroundColor: '#e3f2fd'}}>
      <CardContent>
        <Typography sx={{ fontSize: 14 }} color="text.secondary" > 
        <InfoRoundedIcon/> User Guide Information
        </Typography>
        <br/>
        <Typography variant="body2">
        For Bastian who is using this for his research, the Robot Radar is an obstacle tracking system that provides a front-end application to extend the GoPiGo platform and offer features that no other proprietary GoPiGo2 systems include, such as obstacle detection capabilities and communication between other GoPiGo robots. and which do not currently have obstacle detection capabilities, nor do they have built-in communication between robots on which obstacles are the same. 
          <br />
        </Typography>
      </CardContent>
     
    </Card>
  );
}