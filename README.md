Examination 
Containerization,20 yhp 

Kunskapskrav 
Kunskaper 
1. Redogöra för vad en container är och vad som skiljer den mot ex. VPS 
2. Redogöra för när det lämpar sig med containers i skapandet av system 
3. Förklara konceptet med Stateless och varför det är en central designprincip vid containerization 
4. Redogöra för vad en microservice-arkitektur är samt när det lämpar sig väl i systemdesign Färdigheter 
5. Skapa och hantera containers i Docker 
6. Driftsätta containers i molnet Kompetenser 
7. Ta ansvar för och självständigt skapa en microservice-tjänst med containers 

Bedömning 
Principer för betygssättning 
Den studerandes prestation betygsätts efter genomförd kurs med betygen Icke Godkänt (IG), Godkänt (G) eller Väl Godkänt (VG). 

Icke godkänt (IG) Den studerande har fullföljt kursen men inte nått alla mål för kursen. 

Godkänt (G) Den studerande har nått samtliga mål för kursen. 

Väl Godkänt (VG) För att få betyget Väl Godkänt (VG) ska den studerande dels ha genomfört kursen och nått alla kursens läranderesultat, dels uppfylla kravet att designa och driftsätta en microservice-tjänst bestående av flera containers. 

Uppgiftsbeskrivning 
Vi har under denna kurs stiftat bekantskap med containers som utvecklings och körmiljö för våra applikationer. Nu har vi kommit till själva uppkörning, att själv utveckla och driftsätta en microservice! 

Val av tekniker avgör ni men följande krav finns. 

För godkänt ska en enklare applikation utvecklas och driftsättas. Det kan vara allt ifrån en webbapplikation till ett enklare API, ex. en todo-app. 
● du ska skapa en egen image av din applikation ( dockerfile + docker build ) 
● din image ska laddas upp på docker hub ( docker push ) 
● driftsättas i molnet ( ex. AWS Fargate eller EC2 ) 

För Väl Godkänt ska din microservice bestå av flera containrar som kommunicerar synkront och asynkront, det kan ex. enklare order-service, en todo-app, eller annan applikation. Utöver kriterierna för Godkänt gäller följande krav: 
● en service bestående av flera containers 
● synkron och / eller asynkron kommunikation mellan containers 

