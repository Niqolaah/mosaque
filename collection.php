<!DOCTYPE html>
<html lang="fr">

<head>
    <meta charset="UTF-8">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<title>Portfolio Artiste</title>

	<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@500&family=Montserrat:wght@300;400&display=swap" rel="stylesheet">
	<link rel="stylesheet" href="sources/hearder_and_body.css">
    <link rel="stylesheet" href="sources/colection.css">

</head>
<body>
    <?php 
		include("header.php")
	?>
    <section class="banner">
        <h1>Collection Mamipheres</h1>
        <p>
            Chaque tableau se construit fragment par fragment. Les pierres naturelles — 
            posées à plat ou sur la tranche — imitent la texture du poil, créant un relief 
            vivant et tactile. Chaque angle, chaque inclinaison modifie la façon dont la 
            lumière effleure la surface, révélant des nuances insoupçonnées.
            Les couleurs sont choisies dans des tonalités qui se fondent les unes dans les 
            autres pour créer une harmonie naturelle. Pas de contraste violent, mais une 
            subtile graduation qui donne à l'œuvre sa profondeur .
            Face à cette rugosité de la pierre, le verre intervient comme une respiration. 
            Sa brillance capte la lumière et la restitue vivante, créant un contraste saisissant 
            entre matité et éclat, entre brut et raffiné. C'est dans ce dialogue entre les matières 
            que chaque tableau trouve son équilibre et sa vibration.
        </p>
    </section>
    <section class="gallery">
        <div class="gallery-container">
            <a href="product.php">
                <figure>
                    <img src="sources/imgs/gorille.jpg" alt="Lorem ipsum dolor sit amet">
                    <figcaption>
                        <div class="overlay-content">
                            <h3>Gorille</h3>
                            <p>En savoir plus ...</p>
                        </div>
                    </figcaption>
                </figure>
            </a>
            <figure>
                <img src="https://images.unsplash.com/photo-1458668383970-8ddd3927deed" alt="Lorem ipsum dolor sit amet">
                <figcaption>
                    <h3>Mountains</h3>
                </figcaption>
            </figure>
            <a href="product.html">
                <figure>
                    <img src="sources/imgs/ganesh.jpg" alt="Lorem ipsum dolor sit amet">
                    <figcaption>
                        <h3>Mountains</h3>
                    </figcaption>
                </figure>
            </a>
            <figure>
                <img src="https://images.unsplash.com/photo-1458668383970-8ddd3927deed" alt="Lorem ipsum dolor sit amet">
                <figcaption>
                    <h3>Mountains</h3>
                </figcaption>
            </figure>
            <figure>
                <img src="sources/imgs/felin.jpg" alt="Lorem ipsum dolor sit amet">
                <figcaption>
                    <h3>Mountains</h3>
                </figcaption>
            </figure>
            <figure>
                <img src="https://images.unsplash.com/photo-1458668383970-8ddd3927deed" alt="Lorem ipsum dolor sit amet">
                <figcaption>
                    <h3>Mountains</h3>
                </figcaption>
            </figure>
            <figure>
                <img src="sources/imgs/singe.jpg" alt="Lorem ipsum dolor sit amet">
                <figcaption>
                    <h3>Mountains</h3>
                </figcaption>
            </figure>
            <figure>
                <img src="https://images.unsplash.com/photo-1458668383970-8ddd3927deed" alt="Lorem ipsum dolor sit amet">
                <figcaption>
                    <h3>Mountains</h3>
                </figcaption>
            </figure>
            <figure>
                <img src="https://images.unsplash.com/photo-1458668383970-8ddd3927deed" alt="Lorem ipsum dolor sit amet">
                <figcaption>
                    <h3>Mountains</h3>
                </figcaption>
            </figure>
            <figure>
                <img src="https://images.unsplash.com/photo-1458668383970-8ddd3927deed" alt="Lorem ipsum dolor sit amet">
                <figcaption>
                    <h3>Mountains</h3>

                </figcaption>
            </figure>
            
        </div>
    </section>
</body>