import * as React from 'react';
import { styled } from '@mui/material/styles';
import Box from '@mui/material/Box';
import Paper from '@mui/material/Paper';
import Grid from '@mui/material/Grid';
import { AppBar, Button, Stack, Toolbar, Typography } from '@mui/material';
import TextField from '@mui/material/TextField';
import FormControlLabel from '@mui/material/FormControlLabel';
import Checkbox from '@mui/material/Checkbox';
import Link from '@mui/material/Link';
import {Routes, Route, useNavigate} from 'react-router-dom';
import InfoCard from '../components/authentication/infoCard';



export default function Login() {
 
  const navigate = useNavigate();

  const gateway = event => {
    event.preventDefault();

    // 👇️ redirect to /contacts
    navigate('/home');
  };
  return (
    <Box sx={{ flexGrow: 1 }}>
        <br/>
      <Grid container spacing={3}>
        <Grid item xs>
        </Grid>
        <Grid item xs={10}>
            <Paper elevation={3}>
         
            <center>

           <AppBar position="static" color='login'>
        <Grid container spacing={1}>
          <Grid item xs={2}>
         <br/>
         
          <Typography variant="h4" component="div" color='#ffffff'sx={{ flexGrow: 1 }}>
           CSC <b>380</b>
         
          </Typography>
          <br/>
          </Grid>
          <Grid item xs={9}>
           
         </Grid>
          </Grid>
          </AppBar>
          <Grid container spacing={1}>
          <Grid item xs={1}>
          
           </Grid>
           <Grid item xs={4}>
           <br/>
         <Box component="form" onSubmit={gateway} noValidate sx={{ mt: 1 }}>
            
           
            <Button
              type="submit"
              fullWidth
              variant="contained"
              sx={{ mt: 3, mb: 2 }}
            >
              Robot Portal
            </Button>
                
          </Box>
           </Grid>
          <Grid item xs={2}>
         
          </Grid>
          <Grid item xs={4}>
            <br/>
          <InfoCard/>
         </Grid>
         <Grid item xs={1}>
           
         </Grid>
          </Grid>
            </center>
            <br/>
           
            </Paper>
        </Grid>
        <Grid item xs>
        </Grid>
      </Grid>
    </Box>
  );
}