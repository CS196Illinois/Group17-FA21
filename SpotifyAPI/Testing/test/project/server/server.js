const express = require('express');
const cors = require('cors')
const bodyParser = require('body-parser')
const SpotifyWebApi = require('spotify-web-api-node');

const app = express()
app.use(cors());
app.use(bodyParser.json())

app.post('/refresh', (req, res) => {
    const refreshToken = req.body.refreshToken
    const spotifyApi = new SpotifyWebApi({
        redirectUri: 'http://localhost:3000',
        clientId: '38812fc98c7040dfb1d054869e69aa1a',
        clientSecret: '468d519302e745ba84f4f6cfe9a7c8e9',
        refreshToken,
    }) 

    spotifyApi
        .refreshAccessToken()
        .then((data) => {
            res.json({
                accessToken: data.body.access_token, 
                expiresIn: data.body.expires_in,
            })
        }).catch(() => {
            res.sendStatus(400)
        })
})

app.post('/login', (req, res) => {
    const code = req.body.code
    const spotifyApi = new SpotifyWebApi({
        redirectUri: 'http://localhost:3000',
        clientId: '38812fc98c7040dfb1d054869e69aa1a',
        clientSecret: '468d519302e745ba84f4f6cfe9a7c8e9'
    }) 

    spotifyApi
        .authorizationCodeGrant(code)
        .then(data => {
            res.json({
                accessToken: data.body.access_token,
                refreshToken: data.body.refresh_token, 
                expiresIn: data.body.expires_in
            })
        })
        .catch(() => {
            res.sendStatus(400)
        })
})

app.listen(3001)

