<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
  <head>
    <link rel="stylesheet" href="../CSS/connection.css">
  </head>
  <body>
    <?php
      $hostname = "cs-class-db.srv.mst.edu";
      $username = "cedtfh";
      $password = "koobpasswordkoobpassword2!";
      $db = "cedtfh";



      $dbconnect=mysqli_connect($hostname,$username,$password,$db);

      if ($dbconnect->connect_error) {
        die("Database connection failed: " . $dbconnect->connect_error);
      }
    ?>

    <div id="allBookWrapper"> 
      <?php
        $all_book_query ="SELECT Book.Title, AUTHOR.Name, Book.Price, Book.Book_ID FROM BOOKS as Book
                            NATURAL JOIN AUTHOR_BOOK
                            JOIN AUTHOR on AUTHOR.AUTHOR_ID = AUTHOR_BOOK.Author_ID
                            WHERE Book.Title IS NOT NULL
                          ORDER BY Title";

        $query = mysqli_query($dbconnect, $all_book_query)
          or die (mysqli_error($dbconnect));

        while ($row = mysqli_fetch_array($query)) {
          echo
          "<div class=\"book\">
            <img src=\"https://placekitten.com/200/139\">
            <td>{$row[0]}</td>
            <td>{$row[1]}</td>
            <td>{$row[2]}</td>
            <td>{$row[3]}</td>
          </div>";
        }

        mysqli_close($dbconnect);
      ?>
    </div>
  </body>
</html>