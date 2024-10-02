# Letterboxd Profile Analyzer

Welcome to my project! It's still in an alpha state, but you can check it out right now on the github pages link. Just submit a letterboxd username and take a look!

## Database
This project uses a postgresql DB to maintain a current look at all relevant movies on letterboxd. To save time on running the app, I pre-scraped a large majority of popular movies. However, your first run could take a few extra seconds if your profile contains movies that aren't currently in the databse. This will minimize over time as more profiles are analyzed.

## Movie Recommendations
Right now I'm using a content based filtering algorithm on genres and themes. It works okay, movie preferences are fairly opaque and genres/themes don't begin to cover them, though letterboxds descriptive themes do help. The plan is to train an SVD model, but the details on assembling the user data needed haven't been implemented yet.

## Immediate planned features:

- Clean up the webpage with more consistent aesthetics
- Add more analytics, there are still a few served by the API that aren't being utilized in the frontend
- Add more interactive functionality, such as allowing the user to investigate analytics further
- Spice up recommendations, even if the content based filtering isn't perfect it can provide the user more information to get the user to investigate the recommended movie further for potential watchability.
- Clean up repo, I'm still working through some roughness of using git on a personal machine
- Visuals, visuals, visuals

## Longer term features:
- Watchlist integration. Have to add more scraping but process should be similar to scraping user profiles.
- Compare with your friends, similar to how spotify does it.
- Movie posters and actor pictures. Could use the TMDB API or scrape from letterboxd as well.
- Better recommendations, maybe using SVD.
