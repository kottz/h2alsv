# Web UI

The main user interface is a responsive web app written in React. The app is
bootstrapped with Facebook's [create-react-app](https://create-react-app.dev). 

## Starting the development server
To start the development server go to the `web_ui` folder in `/src` and run

```bash
npm start
```

## Deployment
To build a minified version ready for production run
```bash
npm run build
```
This will output a deployable version to the `build/` folder.

## Good to know

Each sensor is contained in its own React component. The websocket updates
are passed to each sensor module as a prop. The websocket connection is
done in the parent `SensorDisplay` component, updates are stored in
React state.
