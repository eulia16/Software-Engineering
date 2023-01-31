import Box from '@mui/material/Box';
import Grid from '@mui/material/Grid';
import GreetingCard from '../components/home/greetingCard';
import ControlCard from '../components/home/controlCard';
import ConsoleCard from '../components/home/consoleCard';
import RadarCard from '../components/home/radarCard';
import PanoCard from '../components/home/panoramicCard';
import React from 'react'


export default function Home() {
  return (
    
    <Box sx={{ flexGrow: 1 }}>
        <br/>
      <Grid container spacing={3} padding={2}>
        <Grid item xs={3}>
            <GreetingCard/>
              <br/>
            <ControlCard/>
              <br/>
            <ConsoleCard/>  
        </Grid>
        <Grid item xs={6}>
          <RadarCard/>
        </Grid>
        <Grid item xs={3}>
            <PanoCard/>
        </Grid>
      </Grid>
    </Box>
  );
}