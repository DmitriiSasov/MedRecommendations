<!DOCTYPE html>
<html lang="en" dir="ltr">
  <head>
    <link rel="stylesheet"
    href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css"
    integrity="sha384-9aIt2nRpC12Uk9gS9baDl411NQApFmC26EwAOH8WgZl5MYYxFfc+NcPb1dKGj7Sk"
    crossorigin="anonymous">
    <link rel="stylesheet" href="style.css">
    <meta charset="utf-8">
    <title>КлинРек</title>
  </head>
  <body>
    <div class="navbar navbar-light d-flex justify-content-betweenr myshadow" style="background-color: #08e8de">
      <div class="p-2">
        <h1 align="center">Клинические рекомендации</h1>
      </div>
    </div>
    <div class="container myshadow" style="background-color: #08e8de; width: 500pt;
    border-radius: 5pt; margin-top: 100pt">
      <form class="" action="/search" method="post">
        <div class="form-group" style="padding: 15pt">
          <label for="codes_input" style="font-size: 16pt">Коды МКБ-10</label>
          <input type="text" name="search_req" class="form-control" id="codes_input" style="font-size: 14pt;
          margin-top: 5pt" placeholder="Введите коды МКБ-10">
          <button type="submit" class="btn btn-primary" style="margin-top: 35pt; font-size: 14pt">Сформировать документ</button>
        </div>
      </form>
    </div>
    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"
    integrity="sha384-DfXdz2htPH0lsSSs5nCTpuj/zy4C+OGpamoFVy38MVBnE+IbbVYUew+OrCXaRkfj"
    crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js"
    integrity="sha384-Q6E9RHvbIyZFJoft+2mJbHaEWldlvI9IOYy5n3zV9zzTtmI3UksdQRVvoxMfooAo"
    crossorigin="anonymous"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/js/bootstrap.min.js"
    integrity="sha384-OgVRvuATP1z7JjHLkuOU7Xw704+h835Lr+6QL9UvYjZE3Ipu6Tp75j7Bh/kR0JKI"
    crossorigin="anonymous"></script>
  </body>
</html>