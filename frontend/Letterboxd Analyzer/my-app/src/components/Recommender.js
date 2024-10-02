import { UnorderedList, ListItem } from "@chakra-ui/react";
import React, { useEffect, useState } from "react"


const Recommender = ( { username } ) => {
    const [data, setData] = useState([])
    const [error, setError] = useState(null);
    const [ids, setIDs] = useState([])

    const dataArray = Object.values(data)

    useEffect(() => {

        async function fetchRecommended() {
            try {
                const response = await fetch(`hhttps://letterboxdscrape-a8e5d12dd546.herokuapp.com/recommend/${username}`);
        
                if (response.status === 404) {
                    setError('Username not found')
                    return
                }
                const data = await response.json();
                setData(Object.values(data)); 
                setError(null);
    
            } catch (error) {
                console.error('Error fetching user data:', error);
            }
        }

        if (username) {
            fetchRecommended()
        }
    }, [username])

    useEffect(() => {
        if (data.length > 0) {
          const generateRandomIDs = () => {
            const newIDs = [];
            while (newIDs.length < 5) {
              const rand = Math.floor(Math.random() * data.length);
              if (!newIDs.includes(rand)) {
                newIDs.push(rand);
              }
            }
            setIDs(newIDs);  
          };
    
          generateRandomIDs();
        }
      }, [data]); 

    if (data.length > 0 && ids.length > 0) {
        return (
            <div>
                <UnorderedList>
                    {ids.map((id) => <ListItem>{data[id]['title']}</ListItem>)}
                </UnorderedList>
            </div>
        )
    } else {
        return <div>No Data</div>
    }
}

export default Recommender;