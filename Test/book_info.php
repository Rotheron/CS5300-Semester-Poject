<?php
$hostname = "cs-class-db.srv.mst.edu";
$username = "cedtfh";
$password = "koobpasswordkoobpassword2!";
$db = "cedtfh";
$dbconnect=mysqli_connect($hostname,$username,$password,$db);

#print_r($_GET['BookID']);
$bookID = $_GET['BookID'];

$book_info = "SELECT Book.Title, AUTHOR.Name, Book.Price, Book.Book_ID, BOOK_INFO.ISBN_10, BOOK_INFO.Pub_Date FROM BOOKS as Book 
                    NATURAL JOIN AUTHOR_BOOK
                    JOIN AUTHOR on AUTHOR.AUTHOR_ID = AUTHOR_BOOK.Author_ID
                    JOIN BOOK_INFO on BOOK_INFO.Book_Info_ID = Book.Book_Info_ID
                    WHERE Book.Title IS NOT NULL
                    AND Book.Price IS NOT NULL
                    AND Book.Book_ID like $bookID
                    ORDER BY Book.Title ";
$res_data = mysqli_query($dbconnect,$book_info)or die(mysqli_error($dbconnect));
while($row = mysqli_fetch_array($res_data)){
    for ($x = 0; $x <= 5; $x++) {
        if($row[$x] == ""){
            $row[$x] = "N/A";
        }
      } 
    echo "
        <div class=\"modalBook\">
            <img src=\"http://covers.openlibrary.org/b/isbn/{$row[4]}.jpg\" class=\"modalBookImg\">
            <div class=\"modalBookText\">
                <div><p>Title: {$row[0]}</p></div>
                <div><p>Author: {$row[1]}</p></div>
                <div><p>Price: {$row[2]}</p></div> 
                <div><p>Book ID: {$row[3]}</p></div>
                <div><p>ISBN: {$row[4]}</p></div> 
                <div><p>Publish Date: {$row[5]}</p></div> 
            </div>
        </div>";                    
}
?>

