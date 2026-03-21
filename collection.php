<?php
 error_reporting(E_ALL);
ini_set('display_errors', 1);
require __DIR__ . '/sources/db/db.php'
?>

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
        $category_id = (int) $_GET['category'] ?? null;
        if (!$category_id) {
            die("Aucune catégorie sélectionnée");
        }
        $stmt_prod = $pdo->prepare("SELECT * FROM tableaux WHERE id_category = ?");
        $stmt_prod->execute([$category_id]);

        $stmt_cat = $pdo->prepare("SELECT * FROM category WHERE id_category = ?");
        $stmt_cat->execute([$category_id]);

        $products = $stmt_prod->fetchAll(PDO::FETCH_ASSOC);
        $category = $stmt_cat->fetch(PDO::FETCH_ASSOC);
    ?>
    <section class="banner">
        <h1>Collection <?= $category["name"] ?></h1>
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
            <?php foreach($products as $product): ?>
            <a href="product.php?link=<?= $product["id_product"]?>">
                <figure>
                    <img src="sources/imgs/<?= $product["img_link"]?>">
                    <figcaption>
                        <div class="overlay-content">
                            <h3><?= $product["name"]?></h3>
                            <p>En savoir plus ...</p>
                        </div>
                    </figcaption>
                </figure>
            </a>
            <?php endforeach?>
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