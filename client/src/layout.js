import { Box, Link, Typography } from "@mui/material";
import React from "react";
import {Outlet} from "react-router-dom";
import Tophat from "./components/topHat";


const Layout = () => {
  return (
    <>
     <Tophat/>
     <Outlet />
     {/* <Box sx={{ bgcolor: 'background.paper', p: 6 }} component="footer" position="absolute" bottom="0px" left="0px" right="0px">
       <Typography variant="body2" color="text.secondary" align="center">
        {'Copyright © '}
        <Link color="inherit" href="https://oswego.edu/">
          Robot Radar C
        </Link>{' '}
        {new Date().getFullYear()}
        {'.'}
      </Typography>
      </Box> */}
    
    </>
  );
};

export default Layout;