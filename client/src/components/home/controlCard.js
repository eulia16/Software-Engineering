import * as React from 'react';
import { styled } from '@mui/material/styles';
import Paper from '@mui/material/Paper';
import Grid from '@mui/material/Grid';
import Button from '@mui/material/Button';
import ArrowUpwardRoundedIcon from '@mui/icons-material/ArrowUpwardRounded';
import ArrowBackRoundedIcon from '@mui/icons-material/ArrowBackRounded';
import ArrowForwardRoundedIcon from '@mui/icons-material/ArrowForwardRounded';
import ArrowDownwardRoundedIcon from '@mui/icons-material/ArrowDownwardRounded';
import GamepadRoundedIcon from '@mui/icons-material/GamepadRounded';
import { Avatar, CardHeader } from '@mui/material';
import { blueGrey } from '@mui/material/colors';
import axios from 'axios';

export default function ControlCard() {

  const Item = styled(Paper)(({ theme }) => ({
    ...theme.typography.body2,
    padding: theme.spacing(1),
    textAlign: 'center',
    color: theme.palette.text.secondary,
  }));

  React.useEffect(() => {document.addEventListener('keydown', detectKeyDown, true)}, [])

  const detectKeyDown =(e) => {
    console.log("clicked ", e.key)
    if(e.key == 'w'){
      HandleUp()
    }else if(e.key == 's'){
      HandleBack()
    }else if(e.key == 'd'){
      HandleRight()
    }else if(e.key == 'a'){
      HandleLeft()
    }
  }
  const HandleUp = (e) => {
      axios.get('http://<REMOTE IP>:9823/move?password=<PASSWORD>&movekey=W&remote=True')
         .then((response) => {
           console.log(response.data);
         })
         .catch((err) => {
            console.log(err);
         });
 };
 const HandleBack = (e) => {
  axios.get('http://<REMOTE IP>:9823/move?password=<PASSWORD>&movekey=S&remote=True')
     .then((response) => {
       console.log(response.data);
     })
     .catch((err) => {
        console.log(err);
     });
};
const HandleLeft = (e) => {
  axios.get('http://<REMOTE IP>:9823/move?password=<PASSWORD>&movekey=A&remote=True')
     .then((response) => {
       console.log(response.data);
     })
     .catch((err) => {
        console.log(err);
     });
};
const HandleRight = (e) => {
  axios.get('http://<REMOTE IP>:9823/move?password=<PASSWORD>&movekey=D&remote=True')
     .then((response) => {
       console.log(response.data);
     })
     .catch((err) => {
        console.log(err);
     });
};
  return (
    <Paper elevation={3}>
       <CardHeader
        style={{'background': '#b0bec5'}}
        avatar={
          <Avatar sx={{ bgcolor: blueGrey[500] }} aria-label="Camera">
           <GamepadRoundedIcon/>
          </Avatar>
        }
        title="C O N T R O L "
      />
      <br/>
    <Grid container spacing={2}>
  <Grid item xs={6} md={4}>
    <Item elevation={0}></Item>
  </Grid>
  <Grid item xs={6} md={4}>

<Button variant="outlined" onClick={HandleUp}><ArrowUpwardRoundedIcon/></Button>
 

     
 

  </Grid>
  <Grid item xs={6} md={4}>
    <Item elevation={0}></Item>
  </Grid>
  <Grid item xs={6} md={4}>
  <Button variant="outlined" onClick={HandleLeft}><ArrowBackRoundedIcon/></Button>

  </Grid>
  <Grid item xs={6} md={4}>
    <Item elevation={0}></Item>
  </Grid>
  <Grid item xs={6} md={4}>
  <Button variant="outlined" onClick={HandleRight}><ArrowForwardRoundedIcon/></Button>

  </Grid>
  <Grid item xs={6} md={4}>
    <Item elevation={0}></Item>
  </Grid>
  <Grid item xs={6} md={4}>
  <Button variant="outlined" onClick={HandleBack}><ArrowDownwardRoundedIcon/></Button>

  </Grid>
  <Grid item xs={6} md={4}>
    <Item elevation={0}></Item>
  </Grid>
</Grid>
<br/>
    </Paper>
  );
}