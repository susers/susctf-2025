<?php
highlight_file(__FILE__);
Class Main{
    private $flag;
    private $password;
    private $token;

    private $salt;

    function __construct($password){
        $this->password=$password;
        $this->salt=rand(10000,100000);
        $this->token=md5($this->password.$this->salt);
    }
    function __destruct()
    {   $this->salt="you_will_never_get_flag";
        $token=md5($this->password.$this->salt);
        if ($this->token==$token){
            echo $this->flag;
    }

    }
}

Class Flag{
    private $secret;
    private $key;
    function __toString(){
        return $this->secret->decrypt($this->key);
    }
}

Class Secret{
    function decrypt($key){

        return file_get_contents($key);
    }
}

/*This is a deprecated test class that is no longer maintained. Please do not call, instantiate, or make any changes to it.
 */
Class Test_Deprecated{
    /*this test variable is deprecated
    */
    public $test="echo";
    /*this variable is no use again
    */
    protected $deprecated="var_dump";
    /*This is a deprecated method that is no longer maintained. Please do not call, instantiate, or make any changes to it.
     */
    public function __call($deprecated,$arguments){
        $this->test=$deprecated;
        $test=$this->deprecated;
        call_user_func_array($test,$arguments);
    }

}
unserialize($_POST["ser"]);

