import React, { useState } from 'react';
import GenreAnalysis from '../components/GenreAnalysis';
import CastAnalysis from '../components/CastAnalysis';
import UserSearch from '../components/UserSearch';
import RatingsByYear from '../components/BasicAnalysis';
import { Box, Heading, Text, Container } from '@chakra-ui/react';
import DirectorAnalysis from '../components/DirectorAnalysis';
import { Tabs, TabList, TabPanels, Tab, TabPanel, Spinner } from '@chakra-ui/react'



const UserHistory = () => {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);


  const fetchUserData = async (username) => {
    setLoading(true);

    try {
      const response = await fetch(`http://localhost:5000/allfilms/${username}`);

      if (response.status === 404) {
        setError('Username not found')
        return
      }
      const data = await response.json();
      setData(data); 
      setError(null);

    } catch (error) {
      console.error('Error fetching user data:', error);
    }
  };

  if (!data) {
    return (
    <Container>
        <Heading as="h1">Search User Movie Data</Heading>
        <Box>
          <UserSearch fetchUserData={fetchUserData} />
          {loading && <Spinner size="xl" />}
          {error && <Text color="red">{error}</Text>}
        </Box>
        
    </Container>
    )
  }

  return (
    <Container maxW="container.lg"  p={4}>
      <Heading as="h2">Your Movie History</Heading>
      <Tabs>
        <TabList>
          <Tab>Stats</Tab>
          <Tab>Genres</Tab>
          <Tab>Cast</Tab>
          <Tab>Director</Tab>
        </TabList>
        <TabPanels>
          <TabPanel><RatingsByYear data={data} /></TabPanel>
          <TabPanel><GenreAnalysis data={data} /></TabPanel>
          <TabPanel><CastAnalysis data={data} /></TabPanel>
          <TabPanel><DirectorAnalysis data={data} /></TabPanel>
        </TabPanels>
      </Tabs>
    </Container>
  );
};

export default UserHistory;