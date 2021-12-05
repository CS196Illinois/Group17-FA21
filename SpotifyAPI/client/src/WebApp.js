import React, { useEffect } from "react";
import "./WebApp.css";
import "./SpotifyGetPlaylist";
import SpotifyGetPlaylist from "./SpotifyGetPlaylist";

const CLIENT_ID = '38812fc98c7040dfb1d054869e69aa1a'
const REDIRECT_URI = 'http://localhost:3000'
const SPOTIFY_AUTHORIZE_ENDPOINT = "https://accounts.spotify.com/authorize";
const SCOPES = ['user-read-currently-playing', 'user-read-playback-state']
const DELIMITER = "%20"
const SCOPES_URL_PARAM = SCOPES.join(DELIMITER)

const getReturnedParamsFromSpotifyAuth = (hash) => {
    const stringAfterHashtag = hash.substring(1);
    const paramsInUrl = stringAfterHashtag.split("&");
    const paramsSplitUp = paramsInUrl.reduce((accumulater, currentValue) => {
        const [key, value] = currentValue.split("=");
        accumulater[key] = value;
        return accumulater;
    }, {})

    return paramsSplitUp;
}

export default function WebApp() {
    useEffect(() => {
        if(window.location.hash) {
            const {
                access_token,
                expires_in, 
                token_type,
            } = getReturnedParamsFromSpotifyAuth(window.location.hash);

            localStorage.clear();
            localStorage.setItem("accessToken", access_token);
            localStorage.setItem("tokenType", token_type);
            localStorage.setItem("expiresIn", expires_in);
        }
    })
    const handleLogin = () => {
        window.location = `${SPOTIFY_AUTHORIZE_ENDPOINT}?client_id=${CLIENT_ID}&redirect_uri=${REDIRECT_URI}&scope=${SCOPES_URL_PARAM}&response_type=token&show_dialog=true`
    }
    return (
        <div className="container">
            <h1>CS 196</h1>
            <button onClick={handleLogin}>Login to Spotify</button>
            <SpotifyGetPlaylist />
        </div>
    )
}