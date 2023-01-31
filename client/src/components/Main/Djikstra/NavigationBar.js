import { Button, Stack } from "@mui/material";
import React, { Component } from "react";
import RefreshRoundedIcon from '@mui/icons-material/RefreshRounded';
import RouteRoundedIcon from '@mui/icons-material/RouteRounded';
import AltRouteRoundedIcon from '@mui/icons-material/AltRouteRounded';

import BrowserUpdatedRoundedIcon from '@mui/icons-material/BrowserUpdatedRounded';
import LayersClearRoundedIcon from '@mui/icons-material/LayersClearRounded';

export default class NavigationBar extends Component {
  constructor(props) {
    super(props);
    this.state = {};
  }

  hideFixedMenu = () => this.setState({ fixed: false });
  showFixedMenu = () => this.setState({ fixed: true });

  render() {
    const { onVisiualizePressed } = this.props;
    const { getCoordinates } = this.props;
    const { postCoordinates } = this.props;
    const { clearObstacles } = this.props;


    
    return (
      <div>
        
        <Stack direction="row" spacing={2} padding={2}>
        <Button startIcon={<RefreshRoundedIcon />} variant="contained" color="error" onClick={() => window.location.reload(false)}>System Reset</Button>
        <Button startIcon={<LayersClearRoundedIcon />} variant="contained" color="warning" onClick={() => clearObstacles()}>Clear Obstacles</Button>

        <Button startIcon={<BrowserUpdatedRoundedIcon />} variant="contained"  onClick={() => getCoordinates()}>Manual Update</Button>
        <Button startIcon={<RouteRoundedIcon />} variant="contained" onClick={() => onVisiualizePressed()}>Generate Path</Button>
        
        <Button startIcon={<AltRouteRoundedIcon />} variant="contained" color="warning" onClick={() => postCoordinates()}>Execute Path Radar</Button>
        
</Stack>
<br/>
        
      </div>
    );
  }
}
