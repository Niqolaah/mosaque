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
	<link rel="stylesheet" href="sources/product.css">

</head>
<body>
	<?php 
		include("header.php");

        $product_id = (int) $_GET['link'] ?? null;
        if (!$product_id) {
            die("Aucune tableau correspondant");
        }
        $stmt_prod = $pdo->prepare("SELECT * FROM tableaux WHERE id_product = ?");
        $stmt_prod->execute([$product_id]);

        $product = $stmt_prod->fetch(PDO::FETCH_ASSOC);
	?>

	<h1><?= $product["name"]?></h1>
	<div class="img-container">
		<img src="sources/imgs/<?= $product["img_link"]?>" alt="">
	</div>
	<section class="product">
		<div class="btns-container">
			<a href="collection.php?category=<?= $product["id_category"]?>">
				<div class="btn back-btn-content">
					<p>Retour a la gallerie</p>
				</div>
			</a>
			<?php if ($product["status"] == "unsold"):?>
			<a href="<?= $product["art_majeur_link"]?>" target="_blank" rel="noopener noreferrer">
				<div class="btn product-btn-content">
					<p>lien vers Art Majeur</p>
				</div>
			</a>
			<?php else: ?>
				<div class="btn sold-btn">
					<p>Vendu</p>
				</div>
			<?php endif ?>
		</div>
		<p><?= $product["description"]?></p>

		<table>
			<thead>
				<tr>
					<th scope="col">Nom</th>
					<th scope="col">Annee</th>
					<th scope="col">Prix</th>
					<th scope="col" class="dimensions-th">Dimensions</th>
					
				</tr>
			</thead>
			<tbody>
				<tr>
					<td><?= $product["name"]?></td>
					<td><?= $product["year"]?></td>
					<td><?= $product["price"]?>€</td>
					<td><?= $product["size"]?> </td>
				</tr>
			</tbody>
		</table>
	</section>


</body>