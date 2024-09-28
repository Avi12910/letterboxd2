import React from 'react';
import getItemsCountAndRating from '../common/utils';
import { Table, Thead, Tbody, Tr, Th, Td, TableContainer } from '@chakra-ui/react';

const GenreAnalysis = ({ data }) => {
  const [genreCount, genreRating] = getItemsCountAndRating(data, 'genres', 1)
    
  
  const mostWatchedGenres = Object.entries(genreCount)
      .sort(([, countA], [, countB]) => countB - countA)
      .slice(0,22);
      
  const topGenres = Object.entries(genreRating)
      .sort(([, ratingA], [, ratingB]) => ratingB - ratingA)
      .slice(0,15);

  return (
      <div>
          <TableContainer>
              <Table variant="striped" colorScheme="teal">
                  <Thead>
                      <Tr>
                          <Th>Rank</Th>
                          <Th>Genre</Th>
                          <Th>Count</Th>
                      </Tr>
                  </Thead>
                  <Tbody>
                      {mostWatchedGenres.map(([genre, count], index) => (
                          <Tr key={genre}>
                              <Td>{index + 1}</Td>
                              <Td>{genre}</Td>
                              <Td>{count}</Td>
                          </Tr>
                      ))}
                  </Tbody>
              </Table>
              <Table variant="striped" colorScheme="teal">
                  <Thead>
                      <Tr>
                          <Th>Rank</Th>
                          <Th>Genre</Th>
                          <Th>Average Rating</Th>
                      </Tr>
                  </Thead>
                  <Tbody>
                      {topGenres.map(([genre, count], index) => (
                          <Tr key={genre}>
                              <Td>{index + 1}</Td>
                              <Td>{genre}</Td>
                              <Td>{count}</Td>
                          </Tr>
                      ))}
                  </Tbody>
              </Table>
          </TableContainer>
      </div>
  );
};

export default GenreAnalysis;