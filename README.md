<h1>Django Realtime Chat Application</h1>

<h2>
  Features:
</h2>
<ol>
  <li>
    <strong>
      User Management</strong>
    <ol>
      <li>
        Registration</li>
      <li>
        Login</li>
      <li>
        Logout</li>
      <li>
        Forgot Password</li>
      <li>
        Change Password</li>
      <li>
        View accounts</li>
      <li>
        Update account properties</li>
      <li>
        Search for other users</li>
    </ol>
  </li>
  <li>
    <strong>
      Friend System</strong>
    <ol>
      <li>
        Send friend requests</li>
      <li>
        Accept friend requests</li>
      <li>
        Decline friend requests</li>
      <li>
        Cancel friend requests</li>
      <li>
        Remove Friends</li>
    </ol>
  </li>
  <li>
    <strong>
      Public Chatroom</strong>
    <ul>
      <li>
        Build a public chatroom where any authenticated user can chat. (Django Channels &amp; WebSockets)</li>
    </ul>
  </li>
  <li>
    <strong>
      Private Chatroom</strong>
    <ul>
      <li>
        Have 1-on-1 conversations with friends. (Django Channels and WebSockets)</li>
    </ul>
  </li>
  <li>
    <strong>
      Notifications</strong>
    <ul>
      <li>
        Real-time notifications for things like:
        <ol>
          <li>
            Friend requests (Can accept / decline from the notification)</li>
          <li>
            Private chat messages</li>
        </ol>
      </li>
    </ul>
  </li>
  <li>
    <strong>
      Push to Production</strong>
    <ol>
      <li>
        Purchase a domain</li>
      <li>
        Host the website on Digital Ocean / Heroku
        <ul>
          <li>
            There's a lot more involved here than hosting a regular website. We have Redis configuration and Daphne for the sockets.
            <br>
          </li>
        </ul>
      </li>
    </ol>
  </li>
</ol>
