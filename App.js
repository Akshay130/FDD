
import React, { useState, useEffect } from 'react';
import { Text, View, StyleSheet, Button,Platform} from 'react-native';
import { BarCodeScanner } from 'expo-barcode-scanner';
import* as firebase from 'firebase';
import * as Location from 'expo-location';


const firebaseConfig = {
    apiKey: "AIzaSyCubRvqZ_hE_2AYIUQoSiGFXO0O0YvBgZE",
    authDomain: "fir-rn-app-1.firebaseapp.com",
    projectId: "fir-rn-app-1",
    storageBucket: "fir-rn-app-1.appspot.com",
    messagingSenderId: "512427544249",
    appId: "1:512427544249:web:3bd6ca9ad0168484a4d568"
}

const firebaseApp = firebase.initializeApp(firebaseConfig);
const itemRef = firebaseApp.database().ref('/keys');

export default function App() {
  const [hasPermission, setHasPermission] = useState(null);
  const [scanned, setScanned] = useState(false);
  const [location, setLocation] = useState(null);
  const [errorMsg, setErrorMsg] = useState(null);

  useEffect(() => {
    (async () => {
      const { status } = await BarCodeScanner.requestPermissionsAsync();
      setHasPermission(status === 'granted');
      // let { sta } = await Location.requestForegroundPermissionsAsync();
      // if (sta !== 'granted') {
      //   setErrorMsg('Permission to access location was denied');
      //   return;
      // }
      // let location = await Location.getCurrentPositionAsync({});
      // setLocation(location);
    })();
  }, []);

  useEffect(() => {
    (async () => {
      let { status } = await Location.requestForegroundPermissionsAsync();
      if (status !== 'granted') {
        setErrorMsg('Permission to access location was denied');
        return;
      }

      let location = await Location.getCurrentPositionAsync({});
      setLocation(location);
    })();
  }, []);

  let text = 'Waiting..';
  if (errorMsg) {
    text = errorMsg;
  } else if (location) {
    text = JSON.stringify(location);
  }


  const handleBarCodeScanned = ({ data }) => {
    itemRef.on('value', function (snap) {

        let a_ = snap.val();
        for (let x in a_) {
            console.log(x)
            console.log(a_[x])
            if (a_[x] == data){
              setScanned(true);
              alert(`Matched`);
              firebaseApp.database().ref('/loc').push({text});
              itemRef.child(x).remove();
              }
        }

    })
  };

  if (hasPermission === null) {
    return <Text>Requesting for camera permission</Text>;
  }
  if (hasPermission === false) {
    return <Text>No access to camera</Text>;
  }

  return (

    <View style={styles.container}>

      <BarCodeScanner
        onBarCodeScanned={scanned ? undefined : handleBarCodeScanned}
        style={StyleSheet.absoluteFillObject}
      />

      <View style={styles.overlay}>
      <View style={styles.unfocusedContainer}>

      <Text style={styles.text1}>FAKE DRUGS DETECTOR</Text>
      <Text style={styles.text}>NOTE : Each code can be scanned only once.</Text>
      <Text style={styles.text}>Codes whose keys are not in database will be ignored.</Text></View>
      <View style={styles.middleContainer}>
      <View style={styles.unfocusedContainer}></View>
      <View style={styles.focusedContainer}></View>
      <View style={styles.unfocusedContainer}></View>
      </View>
      <View style={styles.unfocusedContainer}></View>
      </View>
      {scanned && <Button title={'Tap to Scan Again'} onPress={() => setScanned(false)} />}

    </View>

  );
}
const opacity = "rgba(0, 0, 0, .6)";
const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#fff',
    position: 'relative',


  },
    overlay: {
position: 'absolute',
top: 0,
left: 0,
right: 0,
bottom: 0,
},
unfocusedContainer: {
flex: 1,
backgroundColor: 'rgba(0,0,0,0.7)',
},
middleContainer: {
flexDirection: 'row',
flex: 1.5,
},
focusedContainer: {
flex: 6,
},
mybtn:{
  padding:10,
  width:160,
  justifyContent:"center"
  },
text:{
  color:"white",
  fontSize:20,
  top: 170,
  left: 20,
  right: 10,
  bottom: 0,
},
text1:{
  color:"red",
  fontSize:20,
  top: 120,
  left: 140,
  right: 10,
  bottom: 0,
}
  });
