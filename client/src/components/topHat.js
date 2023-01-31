import React from 'react';

import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import IconButton from '@mui/material/IconButton';
import Typography from '@mui/material/Typography';
import HelpRoundedIcon from '@mui/icons-material/HelpRounded';
import Badge from '@mui/material/Badge';
import NotificationsIcon from '@mui/icons-material/Notifications';
import SettingsRoundedIcon from '@mui/icons-material/SettingsRounded';


export default function Tophat() {

  return (
      <AppBar position="static" color='secondary'>
        <Toolbar variant='dense'>
         <img alt="Robot Radar" src="C.gif" className='headLogo'/>
          <Typography
            variant="body1"
            noWrap      
          >
            ROBOT<b>RADAR</b>
          </Typography>
        
          <Box sx={{ flexGrow: 1 }} />
          <Box sx={{ display: { xs: 'none', md: 'flex' } }}>         
          </Box>
        </Toolbar>
      </AppBar>
     
  );
}
