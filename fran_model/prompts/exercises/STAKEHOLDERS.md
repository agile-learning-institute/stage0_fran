# Stakeholders 

## Introduction: 
Observe People

## Observe: 
Record each message as an Observation using this schema
```yaml
    type: object
    properties:
        user:
            description: 
            type: word
        name:
            description:
            type: sentence
        title:
            description:
            type: sentence
        text:
            description:
            type: sentence
```
get user name from message, then parse the text from the message into the name, title, or text properties as shown in the following examples.

parse ``Joe in sales`` as
```yaml
name: Joe
title: Sales
```
parse ``Jim the CEO`` as
```yaml
name: Jim
title: CEO
```
parse ``Machinist`` as
```yaml
title: Machinist
```
parse ``Mac Machinist`` as
```yaml
name: Mac
title: Machinist
```
parse ``nonsensical information provided`` as
```yaml
text: nonsensical information provided
```

## Reflect: 
De-Duplicate, merging observations from
```yaml
observations:
    - user: Mike
      name: James
      title: AWS Account Manager
    - user: Betty
      name: J.
      title: AWS Account Manager
```
to
```yaml
observations:
    - user: Mike, Betty
      name: James
      title: AWS Account Manager
```

Group to find Partners, Users, Group Users into Roles

from
```yaml
```
to
```yaml
```

## Make:
Identify Key User with votes, every user types their three favorite names, update observations with ``vote: #User`` tags. Top vote becomes person for Empathy follow-on exercise. All other users that got any votes get a future ``empathy+`` workshop. 
